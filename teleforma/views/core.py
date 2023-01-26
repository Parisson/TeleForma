# -*- coding: utf-8 -*-
# Copyright (c) 2011-2018 Parisson SARL
# Copyright (c) 2011-2018 Guillaume Pellerin

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Guillaume Pellerin <yomguy@parisson.com>
import datetime
import os
import requests
from html import escape
from io import BytesIO

import weasyprint
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.cache import cache

from jsonrpc import jsonrpc_method
from jsonrpc.proxy import ServiceProxy
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from teleforma.models.crfpa import Home, Student, Training
from teleforma.models.notification import Notification, notify
from teleforma.utils import guess_mimetypes

from ..decorators import access_required
from ..models.appointment import Appointment, AppointmentPeriod
from ..models.chat import ChatMessage
from ..models.core import (Conference, ConferencePublication, Course, CourseType, Department,
                           Document, DocumentType, Media, MediaTranscoded,
                           Organization, Period, Professor, WebClassGroup,
                           StreamingServer, LiveStream,
                           get_user_role)
from ..webclass.models import Webclass, WebclassRecord
from .pages import get_page_content

import logging
logger = logging.getLogger('teleforma')
# def render(request, template, data=None, mimetype=None):
#     return django_render(template, data, context_instance=RequestContext(request),
#                          mimetype=mimetype)

# CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 60*60)


def format_courses(courses, course=None, queryset=None, types=None):
    if queryset:
        for c in queryset:
            if c and c.code != 'X':
                courses.append({'course': c, 'types': types.all(),
                                'date': c.date_modified, 'number': c.number})
    elif course:
        if course.code != 'X':
            courses.append({'course': course, 'types': types.all(),
                            'date': course.date_modified, 'number': course.number})
    return courses


def get_courses(user, date_order=False, num_order=False, num_courses=False, period=None):
    cache_key = f"get_courses-{user.id}-{date_order}-{num_order}-{num_courses}-{period and period.id or None}"
    cached_value = cache.get(cache_key)
    if cached_value:
        return cache.get(cache_key)

    if settings.TELEFORMA_E_LEARNING_TYPE == 'CRFPA':
        from teleforma.views.crfpa import get_crfpa_courses
        result = get_crfpa_courses(user, date_order, num_order, period)
        # cache for one hour
        cache.set(cache_key, result, settings.CACHE_TIMEOUT)
        return result

    elif settings.TELEFORMA_E_LEARNING_TYPE == 'AE':
        from teleforma.views.ae import get_ae_courses
        return get_ae_courses(user, date_order, num_order, period)


def get_trainings(user):
    trainings = []

    if not user.is_authenticated:
        return trainings

    professor = user.professor.all()
    student = user.student.all()
    quotas = user.quotas.all()

    if professor or quotas or user.is_staff:
        trainings = Training.objects.filter(available=True)

    elif student:
        student = user.student.get()
        trainings = student.trainings.all()
    return trainings


def get_course_conferences(period, course, course_type, status_min=3):
    conferences = []
    already_added = set()
    # get conference publications
    publications = ConferencePublication.objects.filter(
        period=period,
        conference__course=course,
        conference__course_type=course_type,
        status__gte=status_min).distinct()
    for publication in publications:
        conferences.append(publication.conference)
        already_added.add(publication.conference.id)

    cc = Conference.objects.filter(period=period,
        course=course,
        course_type=course_type,
        status__gte=status_min)
    for conference in cc:
        # do not include conferences with publication rules
        if conference.id not in already_added:
            conferences.append(conference)
    conferences = sorted(conferences, key=lambda c:-c.session_as_int)
    return conferences


def stream_from_file(__file):
    chunk_size = 0x10000
    f = open(__file, 'r')
    while True:
        __chunk = f.read(chunk_size)
        if not len(__chunk):
            f.close()
            break
        yield __chunk


def get_access(obj, courses):
    access = False
    for course in courses:
        if obj.course == course['course']:
            access = True
    return access


access_error = _('Access not allowed.')
contact_message = _(
    'Please login or contact the website administator to get a private access.')


def get_host(request):
    host = request.META['HTTP_HOST']
    if ':' in host:
        host = host.split(':')[0]
    if host == 'localhost':
        host = '127.0.0.1'
    return host


def get_periods(request):
    user = request.user
    periods = []
    professor = user.professor.all()
    quotas = user.quotas.all()
    students = user.student.all()

    if user.is_superuser or user.is_staff:
        periods = Period.objects.filter(is_open=True)

    elif professor:
        periods = Period.objects.filter(is_open=True)

    elif quotas and not (user.is_superuser or user.is_staff) and not professor:
        periods = []
        for quota in quotas:
            if not quota.period in periods:
                periods.append(quota.period)

    elif students:
        period_ids = request.session.get('period_ids')
        if period_ids:
            periods = [Period.objects.get(id=period_id)
                       for period_id in period_ids]
        else:
            student = user.student.get()
            periods = [training.period for training in student.trainings.all()]
            for period in periods:
                for child in period.children.all():
                    periods.append(child)
            request.session['period_ids'] = [period.id for period in periods]
    else:
        return []

    return periods


def get_default_period(periods):
    if periods:
        return periods[0]
    else:
        period_id = getattr(settings, 'TELEFORMA_PERIOD_DEFAULT_ID', 1)
        default_period = Period.objects.get(id=period_id)
        return default_period


def content_to_pdf(content, dest, encoding='utf-8', **kwargs):
    """
    Write into *dest* file object the given html *content*.
    Return True if the operation completed successfully.
    """
    src = weasyprint.HTML(string=content, encoding=encoding)
    src.write_pdf(dest)
    return True


def content_to_response(content, filename=None):
    """
    Return a pdf response using given *content*.
    """
    response = HttpResponse(content, content_type='application/pdf')
    if filename is not None:
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def render_to_pdf(request, template, context, filename=None, encoding='utf-8',
                  **kwargs):
    """
    Render a pdf response using given *request*, *template* and *context*.
    """
    content = loader.render_to_string(template, context, request=request)
    # return HttpResponse(content)
    buffer = BytesIO()

    succeed = content_to_pdf(content, buffer, encoding, **kwargs)
    if succeed:
        return content_to_response(buffer.getvalue(), filename)
    return HttpResponse('Errors rendering pdf:<pre>%s</pre>' % escape(content))


def serve_media(media_path, content_type="", buffering=True, streaming=False):
    if not content_type:
        content_type = guess_mimetypes(media_path)

    if not settings.DEBUG:
        return nginx_media_accel(media_path, content_type=content_type,
                                 buffering=buffering, streaming=streaming)
    else:
        response = StreamingHttpResponse(
            stream_from_file(media_path), content_type=content_type)
        filename = os.path.basename(media_path)
        if not streaming:
            response['Content-Disposition'] = 'attachment; ' + \
                'filename=' + filename
        return response


def nginx_media_accel(media_path, content_type="", buffering=True, streaming=False):
    """Send a protected media file through nginx with X-Accel-Redirect"""

    response = HttpResponse()
    url = settings.MEDIA_URL + os.path.relpath(media_path, settings.MEDIA_ROOT)
    filename = os.path.basename(media_path)
    if not streaming:
        response['Content-Disposition'] = "attachment; filename=%s" % (
            filename)
    response['Content-Type'] = content_type
    response['X-Accel-Redirect'] = url

    if not buffering:
        response['X-Accel-Buffering'] = 'no'
        #response['X-Accel-Limit-Rate'] = 524288

    return response


def live_message(site, conference):
    token = settings.ADMIN_TOKEN
    requests.post('https://' + site.domain + '/chat/messages',
                  headers={'Authorization': 'Token ' + token},
                  data={'conference_id': conference.id})


class HomeRedirectView(View):

    def get(self, request):
        if request.user.is_authenticated:
            period_id = request.session.get('period_id')
            if not period_id:
                periods = get_periods(request)
                period = get_default_period(periods)
                period_id = period.id
                request.session['period_id'] = period_id
            return HttpResponseRedirect(reverse('teleforma-desk-period-list', kwargs={'period_id': period_id}))
        else:
            return HttpResponseRedirect(reverse('teleforma-login'))


class PeriodAccessMixin(View):

    def get_context_data(self, **kwargs):
        context = super(PeriodAccessMixin, self).get_context_data(**kwargs)
        periods = get_periods(self.request)
        context['periods'] = periods

        if 'period_id' in self.kwargs.keys():
            period_id = int(self.kwargs['period_id'])
            self.period = get_object_or_404(Period, pk=period_id)
        else:
            period = get_default_period(periods)
            period_id = period.id
            self.period = period
        self.request.session['period_id'] = period_id
        context['period'] = self.period
        return context

    def render_to_response(self, context):
        period = context['period']
        if not period in context['periods']:
            messages.warning(self.request, _(
                "You do NOT have access to this resource and then have been redirected to your desk."))
            if self.request.session['period_id'] == period.id:
                del self.request.session['period_id']
            return redirect('teleforma-home')
        return super(PeriodAccessMixin, self).render_to_response(context)

    @jsonrpc_method('teleforma.get_period_list')
    def get_period_list(request, department_id):
        department = Department.objects.get(id=department_id)
        return [period.name for period in Period.objects.filter(department=department)]


class CourseAccessMixin(PeriodAccessMixin):

    def get_context_data(self, **kwargs):
        context = super(CourseAccessMixin, self).get_context_data(**kwargs)
        context['all_courses'] = get_courses(
            self.request.user, num_order=True, period=self.period)
        # If we are a corrector but not a professor, limit object types
        role = get_user_role(self.request.user)
        if role == "corrector":
            context['doc_types'] = DocumentType.objects.filter(
                for_corrector=True)
            context['show_media'] = False
        else:
            context['doc_types'] = DocumentType.objects.all()
            context['show_media'] = True
        context['access_error'] = False
        return context


class CourseListView(CourseAccessMixin, ListView):

    model = Course
    template_name = 'teleforma/courses.html'

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['list_view'] = True

        courses = [course['course'] for course in context['all_courses']]

        # get last published media / document
        last_published = []
        last_media = Media.objects.filter(
            period=self.period, is_published=True, course__in=courses).order_by("-date_added").first()
        if last_media:
            last_published.append(last_media)
        last_document = Document.objects.filter(
            periods=self.period, is_published=True, course__in=courses).order_by("-date_added").first()
        if last_document:
            last_published.append(last_document)
        if last_published:
            last_published = sorted(
                last_published, key=lambda k: k.date_added, reverse=True)[0]
            # get course with the latest published media / document
            for course in context['all_courses']:
                if course['course'].id == last_published.course.id:
                    break
            context['courses'] = [course]
        else:
            # get course with the latest "date"
            context['courses'] = sorted(
                context['all_courses'], key=lambda k: k['date'], reverse=True)[:1]

        user = self.request.user
        is_student = user.student.all().count()
        # appointments_open = False
        appointments = []
        if is_student:
            available_courses = [course['course']
                                 for course in context['all_courses']]
            for appointment in AppointmentPeriod.objects.filter(periods=context['period'], course__in=available_courses):
                if appointment.is_open:
                    found = False
                    for existing in appointments:
                        if existing.course == appointment.course:
                            found = True
                    if not found:
                        appointments.append(appointment)
        context['appointments'] = appointments
        # check if user appointment is next
        user_appointment = Appointment.objects.filter(
            student=user, slot__mode='distance', slot__appointment_period__periods=context['period'])
        if user_appointment:
            user_appointment = user_appointment[0]
            now = datetime.datetime.now()
            # now = datetime.datetime(2020, 10, 29, 9, 00)
            if user_appointment.real_date - datetime.timedelta(hours=1) < now < user_appointment.real_date + datetime.timedelta(hours=1):
                context['current_appointement'] = user_appointment

        homes = Home.objects.filter(enabled=True).order_by('-modified_at')
        for home in homes:
            if home.is_for_period(context['period']):
                context['home_title'] = home.visible_title
                context['home_text'] = home.text
                context['home_video'] = home.video
                break

        if is_student:
            student = user.student.all()[0]
            slots = []
            to_subscribe = []
            student_courses = [course['course']
                               for course in get_courses(user)]
            for webclass in Webclass.published.filter(period=self.period, iej=student.iej, course__in=student_courses):
                # if webclass.course not in student_courses:
                #     continue
                if student.platform_only and not webclass.allow_elearning:
                    continue
                if not student.platform_only and not webclass.allow_presentiel:
                    continue
                if not webclass.is_not_over():
                    continue
                slot = webclass.get_slot(user)
                if slot and slot.status in ('almost', 'ingoing'):
                    slots.append(slot)
                if not slot:
                    to_subscribe.append(webclass)
            context['webclass_slots'] = slots
            context['webclass_to_subscribe'] = to_subscribe
            context['restricted'] = student.restricted

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseListView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.get_course_list')
    def get_course_list(request, organization_name, department_name):
        from teleforma.models import Department, Organization
        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(
            organization=organization, name=department_name)
        return [course.to_dict() for course in Course.objects.filter(department=department)]

    @jsonrpc_method('teleforma.get_course_type_list')
    def get_course_type_list(request):
        return [course_type.to_dict() for course_type in CourseType.objects.all()]

    def pull(request, organization_name, department_name):
        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(
            name=department_name, organization=organization)
        url = 'http://' + department.domain + '/json/'
        s = ServiceProxy(url)

        remote_list = s.teleforma.get_course_list(
            organization_name, department.name)
        for course_dict in remote_list['result']:
            course = Course.objects.filter(code=course_dict['code'])
            if not course:
                course = Course()
            else:
                course = course[0]
            course.from_dict(course_dict)

        remote_list = s.teleforma.get_course_type_list()
        if remote_list['result']:
            for course_type_dict in remote_list['result']:
                course_type = CourseType.objects.filter(
                    name=course_type_dict['name'])
                if not course_type:
                    course_type = CourseType()
                else:
                    course_type = course_type[0]
                course_type.from_dict(course_type_dict)

    @jsonrpc_method('teleforma.get_dep_courses')
    def get_dep_courses(request, id):
        department = Department.objects.get(id=id)
        return [{'id': str(c.id), 'name': str(c)} for c in department.course.all()]

    @jsonrpc_method('teleforma.get_dep_periods')
    def get_dep_periods(request, id):
        department = Department.objects.get(id=id)
        return [{'id': str(c.id), 'name': str(c)} for c in department.period.all()]


class CourseView(CourseAccessMixin, DetailView):

    model = Course

    def get_context_data(self, *args, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        courses = []
        for c in context['all_courses']:
            if c['course'] == course:
                courses = format_courses(
                    courses, course=course, types=c['types'])
        context['courses'] = courses
        # context['notes'] = course.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(
            app_label="teleforma", model="course")

        # webclass
        webclass = None
        webclass_slot = None
        student = self.request.user.student.all()
        if student:
            student = student[0]

        if student:
            try:
                webclass = Webclass.published.filter(
                    period=self.period, course=course, iej=student.iej)[0]
            except IndexError:
                pass
            if webclass:
                if student.platform_only and not webclass.allow_elearning:
                    webclass = None
                elif not student.platform_only and not webclass.allow_presentiel:
                    webclass = None
                else:
                    webclass_slot = webclass.get_slot(self.request.user)
        context['webclass'] = webclass
        context['webclass_slot'] = webclass_slot
        context['webclass_not_over'] = webclass and webclass.is_not_over()

        records = {}
        try:
            records = WebclassRecord.get_records(context['period'], course)
        except Exception as e:
            print(e)
            context['webclass_error'] = True
        context['webclass_records'] = records.get(WebclassRecord.WEBCLASS)
        context['webclass_corrections_records'] = records.get(WebclassRecord.CORRECTION)

        return context

    @method_decorator(access_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.get_course_media_urls')
    def get_course_media_urls(request, id):
        course = Course.objects.get(code=id)
        media_list = []
        for media in course.media.all():
            if media.is_published and media.file and media.conference and 'video' in media.mime_type:
                urls = [{'url': settings.MEDIA_URL +
                         str(media.file), 'mime_type': media.mime_type}]
                for transcoded in media.transcoded.all():
                    urls.append(
                        {'url': settings.MEDIA_URL + str(transcoded.file), 'mime_type': transcoded.mime_type})
                media_list.append(
                    {'session': media.conference.session, 'urls': urls, 'poster': media.poster_url()})
        return media_list


class CoursePendingListView(CourseListView):

    template_name = 'teleforma/courses_pending.html'

    def get_context_data(self, **kwargs):
        context = super(CoursePendingListView, self).get_context_data(**kwargs)
        context['courses'] = sorted(
            context['all_courses'], key=lambda k: k['date'], reverse=True)
        return context


class MediaView(CourseAccessMixin, DetailView):

    model = Media
    template_name = 'teleforma/course_media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaView, self).get_context_data(**kwargs)
        media = self.get_object()
        if not media.mime_type:
            media.set_mime_type()
        context['mime_type'] = media.mime_type
        context['course'] = media.course
        context['type'] = media.course_type
        # context['notes'] = media.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(
            app_label="teleforma", model="course")

        room_name = media.course.code
        if media.conference.web_class_group:
            room_name += '_' + media.conference.public_id

        access = get_access(media, context['all_courses'])
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.publish_media')
    def publish(request, id):
        media = Media.objects.get(id=id)
        media.is_published = True
        media.save()
        for other_media in media.conference.media.all():
            other_media.is_published = True
            other_media.save()
        media.conference.status = 3
        media.conference.date_publish = datetime.datetime.now()
        media.conference.save()

    @jsonrpc_method('teleforma.unpublish_media')
    def unpublish(request, id):
        media = Media.objects.get(id=id)
        media.is_published = False
        media.save()
        for other_media in media.conference.media.all():
            other_media.is_published = False
            other_media.save()
        media.conference.status = 2
        media.conference.save()

    def stream(self, request, period_id, pk, streaming=True):
        courses = get_courses(request.user)
        media = Media.objects.get(id=pk)
        if get_access(media, courses):
            media_path = media.file.path
            return serve_media(media_path, content_type=media.mime_type, streaming=streaming)
        else:
            raise Http404("You don't have access to this media.")

    def download(self, request, period_id, pk):
        return self.stream(request, period_id, pk, streaming=False)


class MediaTranscodedView(CourseAccessMixin, DetailView):

    model = MediaTranscoded
    template_name = 'teleforma/course_media_transcoded.html'

    def get_context_data(self, **kwargs):
        context = super(MediaTranscodedView, self).get_context_data(**kwargs)
        media_transcoded = self.get_object()
        media = media_transcoded.item
        if not media_transcoded.mime_type:
            media_transcoded.set_mime_type()
        context['media'] = media
        context['media_transcoded'] = media_transcoded
        context['mime_type'] = media_transcoded.mime_type
        context['course'] = media.course
        context['type'] = media.course_type
        # context['notes'] = media.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(
            app_label="teleforma", model="course")

        room_name = media.course.code
        if media.conference.web_class_group:
            room_name += '_' + media.conference.public_id

        access = get_access(media, context['all_courses'])
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaTranscodedView, self).dispatch(*args, **kwargs)

    def stream(self, request, period_id, pk, streaming=True):
        courses = get_courses(request.user)
        media = MediaTranscoded.objects.get(id=pk)
        if get_access(media.item, courses):
            media_path = media.file.path
            return serve_media(media_path, content_type=media.mime_type, streaming=streaming)
        else:
            raise Http404("You don't have access to this media.")

    def download(self, request, period_id, pk):
        return self.stream(request, period_id, pk, streaming=False)


class MediaPendingView(ListView):

    model = Media
    template_name = 'teleforma/media_pending.html'

    def get_queryset(self):
        return Media.objects.filter(is_published=False)

    def get_context_data(self, **kwargs):
        context = super(MediaPendingView, self).get_context_data(**kwargs)
        return context

    @method_decorator(permission_required('is_superuser'))
    @method_decorator(access_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaPendingView, self).dispatch(*args, **kwargs)


class MediaViewEmbed(DetailView):

    model = Media
    template_name = 'teleforma/course_media_video_embed.html'


class DocumentView(CourseAccessMixin, DetailView):

    model = Document
    template_name = 'teleforma/course_document.html'

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        document = self.get_object()
        context['course'] = document.course
        # context['notes'] = document.notes.all().filter(author=self.request.user)
        access = get_access(document, context['all_courses'])
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        context['periods'] = get_periods(self.request.user)
        return context

    @method_decorator(access_required)
    def dispatch(self, *args, **kwargs):
        return super(DocumentView, self).dispatch(*args, **kwargs)

    def download(self, request, pk):
        courses = get_courses(request.user)
        document = Document.objects.get(pk=pk)
        if get_access(document, courses):
            return serve_media(document.file.path, streaming=False)
        else:
            return redirect('teleforma-home')

    def view(self, request, pk):
        courses = get_courses(request.user)
        document = Document.objects.get(pk=pk)
        if get_access(document, courses):
            return serve_media(document.file.path, streaming=True)
        else:
            return redirect('teleforma-home')


class ConferenceView(CourseAccessMixin, DetailView):

    model = Conference
    template_name = 'teleforma/course_conference.html'

    def get_context_data(self, **kwargs):
        context = super(ConferenceView, self).get_context_data(**kwargs)
        conference = self.get_object()
        context['course'] = conference.course
        context['type'] = conference.course_type
        # context['notes'] = conference.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(
            app_label="teleforma", model="course")

        room_name = conference.course.code
        if conference.web_class_group:
            room_name += '_' + conference.public_id

        context['livestreams'] = conference.livestream.all()
        context['host'] = get_host(self.request)
        access = get_access(conference, context['all_courses'])
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        return context

    @jsonrpc_method('teleforma.stop_conference')
    def stop(request, public_id):
        conference = Conference.objects.get(public_id=public_id)
        conference.date_end = datetime.datetime.now()
        conference.save()
        for stream in conference.livestream.all():
            stream.delete()
        for station in conference.station.all():
            station.started = False
            station.save()
            station.stop()
        if 'telecaster' in settings.INSTALLED_APPS:
            try:
                url = 'http://' + conference.department.domain + '/json/'
                s = ServiceProxy(url)
                s.teleforma.stop_conference(conference.public_id)
            except:
                pass

    @jsonrpc_method('teleforma.create_conference')
    def create(request, conf_dict):
        if isinstance(conf_dict, dict):
            conferences = Conference.objects.filter(public_id=conf_dict['id'])
            if not conferences:
                conference = Conference()
                conference.from_json_dict(conf_dict)
                conference.save()
                if conference.streaming:
                    for stream in conf_dict['streams']:
                        host = getattr(
                            settings, "TELECASTER_LIVE_STREAMING_SERVER", stream['host'])
                        protocol = getattr(
                            settings, "TELECASTER_LIVE_STREAMING_PROTOCOL", 'http')
                        server_type = stream['server_type']
                        stream_type = stream['stream_type']
                        if server_type == 'icecast':
                            port = getattr(
                                settings, "TELECASTER_LIVE_ICECAST_STREAMING_PORT", '8000')
                            path = getattr(
                                settings, "TELECASTER_LIVE_ICECAST_STREAMING_PATH", '/')
                        elif server_type == 'stream-m':
                            port = getattr(
                                settings, "TELECASTER_LIVE_STREAM_M_STREAMING_PORT", '8080')
                            path = getattr(
                                settings, "TELECASTER_LIVE_STREAM_M_STREAMING_PATH", '/')
                        #site = Site.objects.all()[0]
                        server, c = StreamingServer.objects.get_or_create(
                            protocol=protocol,
                            host=host,
                            port=port,
                            path=path,
                            type=server_type)
                        stream = LiveStream(conference=conference, server=server,
                                            stream_type=stream_type, streaming=True)
                        stream.save()

                    if not conference.web_class_group:
                        try:
                            site = get_current_site(request)
                            live_message(site, conference)
                        except:
                            pass
        else:
            raise 'Error : input must be a conference dictionnary'

    @method_decorator(access_required)
    def dispatch(self, *args, **kwargs):
        return super(ConferenceView, self).dispatch(*args, **kwargs)


class ConferenceListView(View):

    @jsonrpc_method('teleforma.get_conference_list')
    def get_conference_list(request):
        conferences = Conference.objects.all()
        return [c.to_json_dict() for c in conferences]

    def pull(request):
        departments = Department.objects.all()
        for department in departments:
            url = 'http://' + department.domain + '/json/'
            s = ServiceProxy(url)
            remote_list = s.teleforma.get_conference_list()
            for conf_dict in remote_list['result']:
                conference = Conference.objects.filter(
                    public_id=conf_dict['id'])
                if not conference:
                    conference = Conference()
                    conference.from_json_dict(conf_dict)

    def push(request, organization_name, department_name):
        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(
            name=department_name, organization=organization)
        url = 'http://' + department.domain + '/json/'
        s = ServiceProxy(url)
        remote_list = s.teleforma.get_conference_list()['result']
        remote_ids = [conf['id'] for conf in remote_list]
        for conference in Conference.objects.all():
            if not conference.public_id in remote_ids and conference.date_end:
                s.teleforma.create_conference(conference.to_json_dict())


@method_decorator(csrf_exempt, name='dispatch')
class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    # deprecated
    def get(self, request):
        """
        Get last 100 messages, in json
        You need to provide a room_name in request
        """
        messages = [message.to_dict() for message in ChatMessage.objects.filter(
            room_name=request.GET['room_name']).order_by('-created')[:100]]
        messages = messages[::-1]
        return Response(messages)

    def post(self, request):
        """
        Send a chat message
        You can pass either : 
        - a conference id 
        - a room name and a message
        """
        room_name = request.POST.get('room_name')
        message = request.POST.get('message')
        if not room_name:
            conference = Conference.objects.get(
                id=request.POST.get('conference_id'))
            ChatMessage.live_conference_message(conference=conference)
        else:
            ChatMessage.add_message(room_name, message, system=True)
        return Response({'status': 'ok'})


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Update a notification (set as read)
        """
        id = request.data.get('id')
        viewed = request.data.get('viewed')
        notif = Notification.objects.get(pk=id)
        notif.viewed = viewed
        notif.save()
        return Response({'status': 'ok'})


class LiveConferenceNotify(APIView):
    def post(self, request):
        """
        notify users a new live conference is starting
        """
        conference_id = request.data.get('id')
        if not conference_id:
            raise Exception('No conference id in request')
        conference = Conference.objects.get(pk=int(conference_id))
        students = Student.objects.filter(period=conference.period, platform_only=True)
        text = f"""Une conférence live "{conference.course.title}" commence"""
        url = reverse('teleforma-conference-detail', kwargs={'period_id': conference.period.id, 'pk': conference.id})
        for student in students:
            try:
                if student.user:
                    courses = get_courses(student.user, period=conference.period)
                    for course in courses:
                        if conference.course == course['course'] and \
                                conference.course_type in course['types']:
                            notify(student.user, text, url)
                            logger.info("Student notified: " + student.user.username)
            except Exception as e:
                logger.warning("Student NOT notified: " + str(student.id))
                logger.warning(e)
        return Response({'status': 'ok'})
        
        



# class ConferenceRecordView(FormView):
#     "Conference record form : TeleCaster module required"

#     model = Conference
#     form_class = ConferenceForm
#     template_name = 'teleforma/course_conference_record.html'
#     hidden_fields = ['started', 'date_begin',
#                      'date_end', 'public_id', 'readers']

#     def get_context_data(self, **kwargs):
#         context = super(ConferenceRecordView, self).get_context_data(**kwargs)
#         context['mime_type'] = 'video/webm'
#         status = Status()
#         status.update()
#         context['hidden_fields'] = self.hidden_fields
#         context['room'] = get_room(name='monitor')
#         return context

#     def get_success_url(self):
#         return reverse('teleforma-conference-detail', kwargs={'period_id': self.conference.period.id,
#                                                               'pk': self.conference.id})

#     def form_valid(self, form):
#         form.save()
#         uuid = get_random_hash()
#         conference = form.instance
#         conference.date_begin = datetime.datetime.now()
#         conference.public_id = uuid
#         conference.save()
#         self.conference = conference
#         status = Status()
#         status.get_hosts()

#         stations = settings.TELECASTER_CONF
#         for station in stations:
#             type = station['type']
#             conf = station['conf']
#             port = station['port']
#             server_type = station['server_type']
#             server, c = StreamingServer.objects.get_or_create(
#                 host=status.ip, port=port, type=server_type)
#             station = Station(conference=conference, public_id=uuid)
#             station.setup(conf)
#             try:
#                 station.start()
#             except:
#                 continue
#             station.save()
#             stream = LiveStream(conference=conference, server=server,
#                                 stream_type=type, streaming=True)
#             stream.save()
#             if server_type == 'stream-m':
#                 try:
#                     self.snapshot(
#                         'http://localhost:8080/snapshot/monitor', station.output_dir)
#                 except:
#                     pass

#         try:
#             live_message(self.conference)
#         except:
#             pass

#         try:
#             self.push()
#         except:
#             pass

#         return super(ConferenceRecordView, self).form_valid(form)

#     def snapshot(self, url, dir):
#         width = 160
#         height = 90
#         img = urllib.urlopen(url)
#         path = dir + os.sep + 'preview.webp'
#         f = open(path, 'w')
#         f.write(img.read())
#         f.close()
#         command = 'dwebp ' + path + ' -o ' + dir + os.sep + 'preview.png &'
#         os.system(command)

#     @method_decorator(access_required)
#     def dispatch(self, *args, **kwargs):
#         return super(ConferenceRecordView, self).dispatch(*args, **kwargs)

#     @jsonrpc_method('teleforma.create_conference')
#     def create(request, conf_dict):
#         if isinstance(conf_dict, dict):
#             conferences = Conference.objects.filter(public_id=conf_dict['id'])
#             if not conferences:
#                 conference = Conference()
#                 conference.from_json_dict(conf_dict)
#                 conference.save()

#                 if conference.streaming:
#                     for stream in conf_dict['streams']:
#                         host = getattr(
#                             settings, "TELECASTER_LIVE_STREAMING_SERVER", stream['host'])
#                         server_type = stream['server_type']
#                         stream_type = stream['stream_type']
#                         if server_type == 'icecast':
#                             port = getattr(
#                                 settings, "TELECASTER_LIVE_ICECAST_STREAMING_PORT", stream['port'])
#                         elif server_type == 'stream-m':
#                             port = getattr(
#                                 settings, "TELECASTER_LIVE_STREAM_M_STREAMING_PORT", stream['port'])
#                         #site = Site.objects.all()[0]
#                         server, c = StreamingServer.objects.get_or_create(host=host,
#                                                                           port=port,
#                                                                           type=server_type)
#                         stream = LiveStream(conference=conference, server=server,
#                                             stream_type=stream_type, streaming=True)
#                         stream.save()

#                     if not conference.web_class_group:
#                         try:
#                             live_message(conference)
#                         except:
#                             pass
#         else:
#             raise 'Error : input must be a conference dictionnary'

#     def push(self):
#         url = 'http://' + self.conference.department.domain + '/json/'
#         s = ServiceProxy(url)
#         s.teleforma.create_conference(self.conference.to_json_dict())


class ProfessorListView(View):

    @jsonrpc_method('teleforma.get_professor_list')
    def get_professor_list(request):
        professors = Professor.objects.all()
        return [p.to_json_dict() for p in professors]

    def pull(request, host=None):
        if host:
            url = 'http://' + host + '/json/'
        else:
            url = 'http://' + settings.TELECASTER_MASTER_SERVER + '/json/'
        s = ServiceProxy(url)

        remote_list = s.teleforma.get_professor_list()
        for professor_dict in remote_list['result']:
            user, c = User.objects.get_or_create(
                username=professor_dict['username'])
            user.first_name = professor_dict['first_name']
            user.last_name = professor_dict['last_name']
            user.email = professor_dict['email']
            user.save()

            professor, c = Professor.objects.get_or_create(user=user)
            for course_code in professor_dict['courses']:
                course = Course.objects.filter(code=course_code)
                if course:
                    if not course[0] in professor.courses.all():
                        professor.courses.add(course[0])
            professor.save()


class WebClassGroupView(View):

    @jsonrpc_method('teleforma.get_class_group_list')
    def get_class_group_list(request):
        class_groups = WebClassGroup.objects.all()
        return [w.to_json_dict() for w in class_groups]

    def pull(request, host=None):
        if host:
            url = 'http://' + host + '/json/'
        else:
            url = 'http://' + settings.TELECASTER_MASTER_SERVER + '/json/'
        s = ServiceProxy(url)

        remote_list = s.teleforma.get_class_group_list()
        for class_group_dict in remote_list['result']:
            class_group, c = WebClassGroup.objects.get_or_create(
                name=class_group_dict['name'])


class HelpView(TemplateView):

    template_name = 'teleforma/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['page_content'] = get_page_content(self.request, 'help',
                                                   ignore_slash_issue=True)
        return context

    def dispatch(self, *args, **kwargs):
        return super(HelpView, self).dispatch(*args, **kwargs)


class PDFTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for Django class based views.
    Switch normal and pdf template based on request.

    The switch is made when the request has a particular querydict, e.g.::

        http://www.example.com?format=pdf

    The key and value of the querydict can be overridable using *as_view()*.
    That pdf url will be present in the context as *pdf_url*.

    For example it is possible to define a view like this::

        from django.views.generic import View

        class MyView(PDFTemplateResponseMixin, View):
            template_name = 'myapp/myview.html'
            pdf_filename = 'report.pdf'

    The pdf generation is automatically done by *weasyprint* using
    the *myapp/myview_pdf.html* template.

    Note that the pdf template takes the same context as the normal template.
    """
    pdf_template_name = None
    pdf_template_name_suffix = '_pdf'
    pdf_querydict_key = 'format'
    pdf_querydict_value = 'pdf'
    pdf_encoding = 'utf-8'
    pdf_filename = None
    pdf_url_varname = 'pdf_url'
    pdf_kwargs = {}

    def is_pdf(self):
        value = self.request.REQUEST.get(self.pdf_querydict_key, '')
        return value.lower() == self.pdf_querydict_value.lower()

    def _get_pdf_template_name(self, name):
        base, ext = os.path.splitext(name)
        return '%s%s%s' % (base, self.pdf_template_name_suffix, ext)

    def get_pdf_template_names(self):
        """
        If the template name is not given using the class attribute
        *pdf_template_name*, then it is obtained using normal template
        names, appending *pdf_template_name_suffix*, e.g.::

            path/to/detail.html -> path/to/detail_pdf.html
        """
        if self.pdf_template_name is None:
            names = super(PDFTemplateResponseMixin, self).get_template_names()
            return map(self._get_pdf_template_name, names)
        return [self.pdf_template_name]

    def get_pdf_filename(self):
        """
        Return the pdf attachment filename.
        If the filename is None, the pdf will not be an attachment.
        """
        return self.pdf_filename

    def get_pdf_url(self):
        """
        This method is used to put the pdf url in the context.
        """
        querydict = self.request.GET.copy()
        querydict[self.pdf_querydict_key] = self.pdf_querydict_value
        return '%s?%s' % (self.request.path, querydict.urlencode())

    def get_pdf_response(self, context, **response_kwargs):
        return render_to_pdf(
            request=self.request,
            template=self.get_pdf_template_names(),
            context=context,
            encoding=self.pdf_encoding,
            filename=self.get_pdf_filename(),
            **self.pdf_kwargs
        )

    def render_to_response(self, context, **response_kwargs):
        if self.is_pdf():
            from django.conf import settings
            context['STATIC_ROOT'] = settings.STATIC_ROOT
            return self.get_pdf_response(context, **response_kwargs)
        context[self.pdf_url_varname] = self.get_pdf_url()
        return super(PDFTemplateResponseMixin, self).render_to_response(
            context, **response_kwargs)
