# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Parisson SARL

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
    if settings.TELEFORMA_E_LEARNING_TYPE == 'CRFPA':
        from teleforma.views.crfpa import format_crfpa_courses
        return format_crfpa_courses(courses, course, queryset, types)
    
    elif settings.TELEFORMA_E_LEARNING_TYPE == 'AE':
        from teleforma.views.ae import format_ae_courses
        return format_ae_courses(courses, course, queryset, types)
    

def get_courses(user, date_order=False, num_order=False):
    if settings.TELEFORMA_E_LEARNING_TYPE == 'CRFPA':
        from teleforma.views.crfpa import get_crfpa_courses
        return get_crfpa_courses(user, date_order, num_order)
    
    elif settings.TELEFORMA_E_LEARNING_TYPE == 'AE':
        from teleforma.views.ae import get_ae_courses
        return get_ae_courses(user, date_order, num_order)
    

def stream_from_file(__file):
    chunk_size = 0x10000
    f = open(__file, 'r')
    while True:
        __chunk = f.read(chunk_size)
        if not len(__chunk):
            f.close()
            break
        yield __chunk


def get_room(content_type=None, id=None, name=None):
    rooms = jqchat.models.Room.objects.filter(content_type=content_type,
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
    return host


def get_random_hash():
    hash = random.getrandbits(128)
    return "%032x" % hash

def get_periods(user):
    periods = None

    professor = user.professor.all()
    if professor:
        professor = user.professor.get()
        periods = Period.objects.all()

    if settings.TELEFORMA_E_LEARNING_TYPE == 'CRFPA':
        student = user.student.all()
        if student:
            student = user.student.get()
            periods = student.period.all() 

    elif settings.TELEFORMA_E_LEARNING_TYPE == 'AE':
        student = user.ae_student.all()
        if student:
            student = user.ae_student.get()
            periods = student.period.all()

    if user.is_staff or user.is_superuser:
        periods = Period.objects.all()
    
    return periods
    

class CourseView(DetailView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        all_courses = get_courses(self.request.user, num_order=True)
        courses = []
        for c in all_courses:
            if c['course'] == course:
                courses = format_courses(courses, course=course, types=c['types'])
        context['courses'] = courses
        context['all_courses'] = all_courses
        context['notes'] = course.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="course")
        if settings.TELEFORMA_GLOBAL_TWEETER:
            context['room'] = get_room(name='site')
        else:
            context['room'] = get_room(name=course.title, content_type=content_type,
                                   id=course.id)
        context['doc_types'] = DocumentType.objects.all()
        context['periods'] = get_periods(self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseView, self).dispatch(*args, **kwargs)


class CoursesView(ListView):

    model = Course
    template_name='teleforma/courses.html'

    def get_queryset(self):
        self.all_courses = get_courses(self.request.user, date_order=True)
        return self.all_courses[:10]

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(author=self.request.user)
        context['room'] = get_room(name='site')
        context['doc_types'] = DocumentType.objects.all()
        context['all_courses'] = sorted(self.all_courses, key=lambda k: k['number'])
        context['periods'] = get_periods(self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CoursesView, self).dispatch(*args, **kwargs)


class MediaView(DetailView):

    model = Media
    template_name='teleforma/course_media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaView, self).get_context_data(**kwargs)
        all_courses = get_courses(self.request.user)
        context['all_courses'] = all_courses
        media = self.get_object()
        if not media.mime_type:
            media.set_mime_type()
        context['mime_type'] = media.mime_type
        context['course'] = media.course
        context['item'] = media.item
        context['type'] = media.course_type
        context['notes'] = media.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="media")
        if settings.TELEFORMA_GLOBAL_TWEETER:
            context['room'] = get_room(name='site')
        else:
            context['room'] = get_room(name=media.item.title, content_type=content_type,
                                   id=media.id)
        access = get_access(media, all_courses)
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        context['periods'] = get_periods(self.request.user)
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
            return redirect('teleforma-media-detail', media.id)


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


class DocumentView(DetailView):

    model = Document
    template_name='teleforma/course_document.html'

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        all_courses = get_courses(self.request.user)
        context['all_courses'] = all_courses
        document = self.get_object()
        context['course'] = document.course
        context['notes'] = document.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="document")
        if settings.TELEFORMA_GLOBAL_TWEETER:
            context['room'] = get_room(name='site')
        else:
            context['room'] = get_room(name=document.title, content_type=content_type,
                                   id=document.id)
        access = get_access(document, all_courses)
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
            return redirect('teleforma-document-detail', document.id)

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
            return redirect('teleforma-document-detail', document.id)


class ConferenceView(DetailView):

    model = Conference
    template_name='teleforma/course_conference.html'

    def get_context_data(self, **kwargs):
        context = super(ConferenceView, self).get_context_data(**kwargs)
        all_courses = get_courses(self.request.user)
        context['all_courses'] = all_courses
        conference = self.get_object()
        context['course'] = conference.course
        context['type'] = conference.course_type
        context['notes'] = conference.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="conference")
        if settings.TELEFORMA_GLOBAL_TWEETER:
            context['room'] = get_room(name='site')
        else:
            context['room'] = get_room(name=conference.course.title, content_type=content_type,
                                   id=conference.id)
        context['livestreams'] = conference.livestream.all()
        context['host'] = get_host(self.request)
        access = get_access(conference, all_courses)
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        context['periods'] = get_periods(self.request.user)
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


class ConferenceRecordView(FormView):
    "Conference record form : telecaster module required"

    model = Conference
    form_class = ConferenceForm
    template_name='teleforma/course_conference_record.html'
    hidden_fields = ['started', 'date_begin', 'date_end', 'public_id', 'readers']

    def get_context_data(self, **kwargs):
        context = super(ConferenceRecordView, self).get_context_data(**kwargs)
        context['all_courses'] = get_courses(self.request.user)
        context['mime_type'] = 'video/webm'
        status = Status()
        status.update()
        
        request_host = get_host(self.request)
        local_host = status.ip
        if request_host.split('.')[0] == local_host.split('.')[0]:
            ip = local_host
        else:
            ip = settings.ROUTER_IP

        context['host'] = ip
        context['hidden_fields'] = self.hidden_fields
        return context

    def get_success_url(self):
        return reverse('teleforma-conference-detail', kwargs={'pk':self.conference.id})

    def form_valid(self, form):
        form.save()
        uuid = get_random_hash()
        self.conference = form.instance
        self.conference.date_begin = datetime.datetime.now()
        self.conference.public_id = uuid
        self.conference.save()
        status = Status()
        status.get_hosts()

        stations = settings.TELECASTER_CONF
        for station in stations:
            type = station['type']
            conf = station['conf']
            port = station['port']
            server_type = station['server_type']
            server, c = StreamingServer.objects.get_or_create(host=status.ip, port=port, type=server_type)
            station = Station(conference=self.conference, public_id=uuid)
            station.setup(conf)
            station.start()
            station.save()
            stream = LiveStream(conference=self.conference, server=server,
                            stream_type=type, streaming=True)
            stream.save()
            if server_type == 'stream-m':
                #FIXME:
#                self.snapshot(stream.snapshot_url, station.output_dir)
                self.snapshot('http://localhost:8080/snapshot/safe', station.output_dir)

        try:
            self.push(self.conference)
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
        command = '/usr/bin/dwebp ' + path + ' -o ' + dir + os.sep + 'preview.png &'
        os.system(command)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConferenceRecordView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.create_conference')
    def create(request, conference):
        if isinstance(conference, dict):
            course = Course.objects.get(code=conference['course_code'])
            if conference['course_type']:
                course_type = CourseType.objects.get(name=conference['course_type'])
            else:
                course_type, cc = CourseType.objects.get_or_create(name='None')

            conf, c = Conference.objects.get_or_create(public_id=conference['id'],
                                                       course=course, course_type=course_type)
            if c:
                conf.session = conference['session']
                if conference['professor_id']:
                    user = User.objects.filter(username=conference['professor_id'])
                    if user:
                        conf.professor = Professor.objects.get(user=user[0])
                    else:
                        user = User(username=conference['professor_id'])
                        user.save()
                        professor = Professor(user=user)
                        professor.save()
                        conf.professor = professor
                try:
                    organization, c = Organization.objects.get_or_create(name=conference['organization'])
                    conf.room, c = Room.objects.get_or_create(name=conference['room'],
                                                       organization=organization)
                except:
                    pass

                conf.date_begin = datetime.datetime.now()
                conf.period, c = Period.objects.get_or_create(name=conference['period'])
                conf.department, c = Department.objects.get_or_create(name=conference['department'])
                conf.save()
                course.save()
                for stream in conference['streams']:
                    host = stream['host']
                    port = stream['port']
                    server_type = stream['server_type']
                    stream_type = stream['stream_type']
                    site = Site.objects.all()
                    server, c = StreamingServer.objects.get_or_create(host=site[0],
                                                                      port=port,
                                                                      type=server_type)
                    stream = LiveStream(conference=conf, server=server,
                                        stream_type=stream_type, streaming=True)
                    stream.save()
        else:
            raise 'Error : Bad Conference dictionnary'

    def push(self, conference):
        url = 'http://' + conference.department.domain + '/json/'
        s = ServiceProxy(url)
        s.teleforma.create_conference(conference.to_json_dict())


class HelpView(TemplateView):

    template_name='teleforma/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['page_content'] = pages.get_page_content(self.request, 'help',
                                                         ignore_slash_issue=True)
        return context

    def dispatch(self, *args, **kwargs):
        return super(HelpView, self).dispatch(*args, **kwargs)


