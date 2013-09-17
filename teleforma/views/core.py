# -*- coding: utf-8 -*-
# Copyright (c) 2011-2013 Parisson SARL

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

import mimetypes
import datetime
import random
import urllib
import urllib2
import json

from jsonrpc import jsonrpc_method

from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, get_backends
from django.template import RequestContext, loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import *
from django.views.generic.base import *
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from jsonrpc.proxy import ServiceProxy

from teleforma.models import *
from teleforma.forms import *
from telemeta.views import *
import jqchat.models
from xlwt import Workbook

try:
    from telecaster.models import *
    from telecaster.tools import *
except:
    pass


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
    if settings.TELEFORMA_E_LEARNING_TYPE == 'CRFPA':
        from teleforma.views.crfpa import get_crfpa_courses
        return get_crfpa_courses(user, date_order, num_order, period)

    elif settings.TELEFORMA_E_LEARNING_TYPE == 'AE':
        from teleforma.views.ae import get_ae_courses
        return get_ae_courses(user, date_order, num_order, period)


def stream_from_file(__file):
    chunk_size = 0x10000
    f = open(__file, 'r')
    while True:
        __chunk = f.read(chunk_size)
        if not len(__chunk):
            f.close()
            break
        yield __chunk


def get_room(content_type=None, id=None, name=None, period=None):
    if settings.TELEFORMA_GLOBAL_TWEETER:
        name = 'site'

    if settings.TELEFORMA_PERIOD_TWEETER and period:
        name = name + '-' + period 

    if settings.TELEFORMA_GLOBAL_TWEETER:
        rooms = jqchat.models.Room.objects.filter(name=name[:20])
    else:
        rooms = jqchat.models.Room.objects.filter(name=name[:20],
                                                  content_type=content_type,
                                                  object_id=id)
    if not rooms:
        room = jqchat.models.Room.objects.create(content_type=content_type,
                                                 object_id=id,
                                                 name=name[:20])
    else:
        room = rooms[0]
    return room

def get_access(obj, courses):
    access = False
    for course in courses:
        if obj.course == course['course']:
            access = True
    return access

access_error = _('Access not allowed.')
contact_message = _('Please login or contact the website administator to get a private access.')

def get_host(request):
    host = request.META['HTTP_HOST']
    if ':' in host:
        host = host.split(':')[0]
    if host == 'localhost':
        host = '127.0.0.1'
    return host

def get_periods(user):
    student = user.student.all()
    if student:
        student = user.student.get()
        periods = [training.period for training in student.trainings.all()]

    if user.is_superuser or user.is_staff:
        periods = Period.objects.all()

    professor = user.professor.all()
    if professor:
        professor = user.professor.get()
        periods = Period.objects.all()

    return periods


class HomeRedirectView(View):

    def get(self, request):
        if request.user.is_authenticated():
            periods = get_periods(request.user)
            return HttpResponseRedirect(reverse('teleforma-desk-period-list', kwargs={'period_id': periods[0].id}))
        else:
            return HttpResponseRedirect(reverse('teleforma-login'))


class PeriodAccessMixin(View):

    period = None

    def get_context_data(self, **kwargs):
        context = super(PeriodAccessMixin, self).get_context_data(**kwargs)
        if 'period_id' in self.kwargs.keys():
            period = Period.objects.filter(id=int(self.kwargs['period_id']))
            if period:
                self.period = period[0]
        context['period'] = self.period
        return context

    def render_to_response(self, context):
        period = context['period']
        if not period in get_periods(self.request.user):
            messages.warning(self.request, _("You do NOT have access to this resource and then have been redirected to your desk."))
            return redirect('teleforma-home')
        return super(PeriodAccessMixin, self).render_to_response(context)

    @jsonrpc_method('teleforma.get_period_list')
    def get_period_list(request, department_id):
        department = Department.objects.get(id=department_id)
        return [period.name for period in Period.objects.filter(department=department)]


class CourseAccessMixin(PeriodAccessMixin):

    def get_context_data(self, **kwargs):
        context = super(CourseAccessMixin, self).get_context_data(**kwargs)
        context['all_courses'] = get_courses(self.request.user, num_order=True, period=self.period)
        return context


class CourseListView(CourseAccessMixin, ListView):

    model = Course
    template_name='teleforma/courses.html'

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(author=self.request.user)
        context['room'] = get_room(name='site', period=context['period'].name)
        context['doc_types'] = DocumentType.objects.all()
        context['list_view'] = True
        context['courses'] = sorted(context['all_courses'], key=lambda k: k['date'], reverse=True)[:5]
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseListView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.get_course_list')
    def get_course_list(request, department_id):
        department = Department.objects.get(id=department_id)
        return [course.to_dict() for course in Course.objects.filter(department=department)]

    def pull(request, organization_name, department_name):
        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(name=department_name, organization=organization)
        url = 'http://' + department.domain + '/json/'
        s = ServiceProxy(url)

        remote_list = s.teleforma.get_course_list(organization.name, department.name)
        for course_dict in remote_list['result']:
            course = Course.objects.filter(code=course_dict['code'])
            if not course:
                course = Course()
            else:
                course = course[0]
            course.from_dict(course_dict)
            
    @jsonrpc_method('teleforma.get_dep_courses')
    def get_dep_courses(request, id):
        department = Department.objects.get(id=id)
        return [{'id': str(c.id), 'name': unicode(c)} for c in department.course.all()]

    @jsonrpc_method('teleforma.get_dep_periods')
    def get_dep_periods(request, id):
        department = Department.objects.get(id=id)
        return [{'id': str(c.id), 'name': unicode(c)} for c in department.period.all()]


class CourseView(CourseAccessMixin, DetailView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        courses = []
        for c in context['all_courses']:
            if c['course'] == course:
                courses = format_courses(courses, course=course, types=c['types'])
        context['courses'] = courses
        # context['notes'] = course.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="course")
        context['room'] = get_room(name=course.code, period=context['period'].name,
                                   content_type=content_type,
                                   id=course.id)
        context['doc_types'] = DocumentType.objects.all()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseView, self).dispatch(*args, **kwargs)


class MediaView(CourseAccessMixin, DetailView):

    model = Media
    template_name='teleforma/course_media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaView, self).get_context_data(**kwargs)
        media = self.get_object()
        if not media.mime_type:
            media.set_mime_type()
        context['mime_type'] = media.mime_type
        context['course'] = media.course
        context['item'] = media.item
        context['type'] = media.course_type
        # context['notes'] = media.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="course")
        context['room'] = get_room(name=media.course.code,period=context['period'].name,
                                   content_type=content_type,
                                   id=media.course.id)

        access = get_access(media, context['all_courses'])
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaView, self).dispatch(*args, **kwargs)

    def download(self, request, pk):
        courses = get_courses(request.user)
        media = Media.objects.get(id=pk)
        if get_access(media, courses):
            path = media.item.file.path
            filename, ext = os.path.splitext(path)
            filename = filename.split(os.sep)[-1]
            fsock = open(media.item.file.path, 'r')
            view = ItemView()
            mimetype = view.item_analyze(media.item)
            extension = mimetypes.guess_extension(mimetype)
            if not extension:
                extension = ext
            response = HttpResponse(fsock, mimetype=mimetype)

            response['Content-Disposition'] = "attachment; filename=%s%s" % \
                                             (filename.encode('utf8'), extension)
            return response
        else:
            return redirect('teleforma-media-detail', self.context['period'].id, media.id)


    @jsonrpc_method('teleforma.publish_media')
    def publish(request, id):
        media = Media.objects.get(id=id)
        media.is_published = True
        media.save()

    @jsonrpc_method('teleforma.unpublish_media')
    def unpublish(request, id):
        media = Media.objects.get(id=id)
        media.is_published = False
        media.save()


class MediaPendingView(ListView):

    model = Media
    template_name='teleforma/media_pending.html'

    def get_queryset(self):
        return Media.objects.filter(is_published=False)

    def get_context_data(self, **kwargs):
        context = super(MediaPendingView, self).get_context_data(**kwargs)
        return context

    @method_decorator(permission_required('is_superuser'))
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaPendingView, self).dispatch(*args, **kwargs)


class DocumentView(CourseAccessMixin, DetailView):

    model = Document
    template_name='teleforma/course_document.html'

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DocumentView, self).dispatch(*args, **kwargs)

    def download(self, request, pk):
        courses = get_courses(request.user)
        document = Document.objects.get(id=pk)
        if get_access(document, courses):
            fsock = open(document.file.path, 'r')
            mimetype = mimetypes.guess_type(document.file.path)[0]
            extension = mimetypes.guess_extension(mimetype)
            response = HttpResponse(fsock, mimetype=mimetype)
            response['Content-Disposition'] = "attachment; filename=%s%s" % \
                                             (document.title.encode('utf8'), extension)
            return response
        else:
            return redirect('teleforma-home')

    def view(self, request, pk):
        courses = get_courses(request.user)
        document = Document.objects.get(id=pk)
        if get_access(document, courses):
            fsock = open(document.file.path, 'r')
            mimetype = mimetypes.guess_type(document.file.path)[0]
            extension = mimetypes.guess_extension(mimetype)
            response = HttpResponse(fsock, mimetype=mimetype)
            return response
        else:
            return redirect('teleforma-home')


class ConferenceView(CourseAccessMixin, DetailView):

    model = Conference
    template_name='teleforma/course_conference.html'

    def get_context_data(self, **kwargs):
        context = super(ConferenceView, self).get_context_data(**kwargs)
        conference = self.get_object()
        context['course'] = conference.course
        context['type'] = conference.course_type
        # context['notes'] = conference.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="course")
        context['room'] = get_room(name=conference.course.code, period=context['period'].name,
                                   content_type=content_type,
                                   id=conference.course.id)
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

    @method_decorator(login_required)
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
                conference = Conference.objects.filter(public_id=conf_dict['id'])
                if not conference:
                    conference = Conference()
                    conference.from_json_dict(conf_dict)

    def push(request, organization_name, department_name):
        organization = organization.objects.get(name=organization_name)
        department = Department.objects.get(name=department_name, organization=organization)
        url = 'http://' + department.domain + '/json/'
        s = ServiceProxy(url)
        remote_list = s.teleforma.get_conference_list()['result']
        remote_ids = [conf['id'] for conf in remote_list]
        for conference in Conference.objects.all():
            if not conference.public_id in remote_ids and conference.date_end:
                s.teleforma.create_conference(conference.to_json_dict())


def live_message(conference):
        from jqchat.models import Message
        user, c = User.objects.get_or_create(username='bot')
        content_type = ContentType.objects.get(app_label="teleforma", model="course")
        room = get_room(name=conference.course.code, period=conference.period.name,
                           content_type=content_type,
                           id=conference.course.id)
        text = _("A new live conference has started : ")
        text += 'http://' + Site.objects.all()[0].domain + reverse('teleforma-conference-detail',
                       kwargs={'period_id': conference.period.id, 'pk': conference.id})
        message = Message.objects.create_message(user, room, text)


class ConferenceRecordView(FormView):
    "Conference record form : telecaster module required"

    model = Conference
    form_class = ConferenceForm
    template_name='teleforma/course_conference_record.html'
    hidden_fields = ['started', 'date_begin', 'date_end', 'public_id', 'readers']

    def get_context_data(self, **kwargs):
        context = super(ConferenceRecordView, self).get_context_data(**kwargs)
        context['mime_type'] = 'video/webm'
        status = Status()
        status.update()
        context['hidden_fields'] = self.hidden_fields
        context['room'] = get_room(name='monitor')
        return context

    def get_success_url(self):
        return reverse('teleforma-conference-detail', kwargs={'period_id': self.conference.period.id,
                                                              'pk':self.conference.id})

    def form_valid(self, form):
        form.save()
        uuid = get_random_hash()
        conference = form.instance
        conference.date_begin = datetime.datetime.now()
        conference.public_id = uuid
        conference.save()
        self.conference = conference
        status = Status()
        status.get_hosts()

        stations = settings.TELECASTER_CONF
        for station in stations:
            type = station['type']
            conf = station['conf']
            port = station['port']
            server_type = station['server_type']
            server, c = StreamingServer.objects.get_or_create(host=status.ip, port=port, type=server_type)
            station = Station(conference=conference, public_id=uuid)
            station.setup(conf)
            try:
                station.start()
            except:
                continue
            station.save()
            stream = LiveStream(conference=conference, server=server,
                            stream_type=type, streaming=True)
            stream.save()
            if server_type == 'stream-m':
                try:
                    self.snapshot('http://localhost:8080/snapshot/monitor', station.output_dir)
                except:
                    pass

        try:
            live_message(self.conference)
        except:
            pass

        try:
            self.push()
        except:
            pass

        return super(ConferenceRecordView, self).form_valid(form)

    def snapshot(self, url, dir):
        width = 160
        height = 90
        img = urllib.urlopen(url)
        path = dir + os.sep + 'preview.webp'
        f = open(path, 'w')
        f.write(img.read())
        f.close()
        command = 'dwebp ' + path + ' -o ' + dir + os.sep + 'preview.png &'
        os.system(command)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConferenceRecordView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.create_conference')
    def create(request, conf_dict):
        if isinstance(conf_dict, dict):
            conferences = Conference.objects.filter(public_id=conf_dict['id'])
            if not conferences:
                conference = Conference()
                conference.from_json_dict(conf_dict)
                conference.save()

                for stream in conf_dict['streams']:
                    host = stream['host']
                    port = stream['port']
                    server_type = stream['server_type']
                    stream_type = stream['stream_type']
                    site = Site.objects.all()[0]
                    server, c = StreamingServer.objects.get_or_create(host=site,
                                                                      port=port,
                                                                      type=server_type)
                    stream = LiveStream(conference=conference, server=server,
                                        stream_type=stream_type, streaming=True)
                    stream.save()
                try:
                    live_message(conference)
                except:
                    pass
        else:
            raise 'Error : input must be a conference dictionnary'

    def push(self):
        url = 'http://' + self.conference.department.domain + '/json/'
        s = ServiceProxy(url)
        s.teleforma.create_conference(self.conference.to_json_dict())


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
            user, c = User.objects.get_or_create(username=professor_dict['username'])
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


class HelpView(TemplateView):

    template_name='teleforma/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['page_content'] = pages.get_page_content(self.request, 'help',
                                                         ignore_slash_issue=True)
        return context

    def dispatch(self, *args, **kwargs):
        return super(HelpView, self).dispatch(*args, **kwargs)

