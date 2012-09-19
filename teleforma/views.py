# Create your views here.

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


def render(request, template, data = None, mimetype = None):
    return render_to_response(template, data, context_instance=RequestContext(request),
                              mimetype=mimetype)

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


def get_courses(user, date_order=False, num_order=False):
    courses = []

    if not user.is_authenticated():
        return courses

    professor = user.professor.all()
    student = user.student.all()

    if professor:
        professor = user.professor.get()
        courses = format_courses(courses, queryset=professor.courses.all(),
                                  types=CourseType.objects.all())

    elif student:
        student = user.student.get()
        s_courses = {student.procedure:student.training.procedure,
                           student.written_speciality:student.training.written_speciality,
                           student.oral_speciality:student.training.oral_speciality,
                           student.oral_1:student.training.oral_1,
                           student.oral_2:student.training.oral_2,
                           student.options:student.training.options,
                        }

        for course in s_courses:
            courses = format_courses(courses, course=course,
                               types=s_courses[course])

        synthesis_note = student.training.synthesis_note
        if synthesis_note:
            courses = format_courses(courses,
                            queryset=Course.objects.filter(synthesis_note=True),
                            types=synthesis_note)

        obligation = student.training.obligation
        if obligation:
            courses = format_courses(courses,
                            queryset=Course.objects.filter(obligation=True),
                            types=obligation)

        magistral = student.training.magistral
        if magistral:
            courses = format_courses(courses,
                            queryset=Course.objects.filter(magistral=True),
                            types=magistral)

    elif user.is_staff or user.is_superuser:
        courses = format_courses(courses, queryset=Course.objects.all(),
                    types=CourseType.objects)
    else:
        courses = None

    if date_order:
        courses = sorted(courses, key=lambda k: k['date'], reverse=True)
    if num_order:
        courses = sorted(courses, key=lambda k: k['number'])

    return courses


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
        context['room'] = get_room(name=course.title, content_type=content_type,
                                   id=course.id)
        context['doc_types'] = DocumentType.objects.all()
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
        context['room'] = get_room(name=media.item.title, content_type=content_type,
                                   id=media.id)
        access = get_access(media, all_courses)
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
        context['room'] = get_room(name=document.title, content_type=content_type,
                                   id=document.id)
        access = get_access(document, all_courses)
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
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
        context['room'] = get_room(name=conference.course.title, content_type=content_type,
                                   id=conference.id)
        context['livestreams'] = conference.livestream.all()
        context['host'] = get_host(self.request)
        access = get_access(conference, all_courses)
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
                url = 'http://' + settings.TELECASTER_MASTER_SERVER + '/json/'
                s = ServiceProxy(url)
                s.teleforma.stop_conference(conference.public_id)
            except:
                pass

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConferenceView, self).dispatch(*args, **kwargs)


class ConferenceRecordView(FormView):
    "Conference record form : TeleCaster module required"

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
        context['host'] = status.ip
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
            course_type = CourseType.objects.get(name=conference['course_type'])
            conf, c = Conference.objects.get_or_create(public_id=conference['id'],
                                                       course=course, course_type=course_type)
            if c:
                conf.session = conference['session']
                user = User.objects.get(username=conference['professor_id'])
                conf.professor = Professor.objects.get(user=user)
                try:
                    organization = Organization.objects.get_or_create(name=conference['organization'])
                    conf.room = Room.objects.get_or_create(name=conference['room'],
                                                       organization=organization)
                except:
                    pass

                conf.date_begin = datetime.datetime.now()
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
        url = 'http://' + settings.TELECASTER_MASTER_SERVER + '/json/'
        s = ServiceProxy(url)
        s.teleforma.create_conference(conference.to_json_dict())


class UsersView(ListView):

    model = User
    template_name='telemeta/users.html'
    context_object_name = 'users'
    #paginate_by = 12

    def get_queryset(self):
        return User.objects.all().select_related(depth=1).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        context['trainings'] = Training.objects.all()
        context['iejs'] = IEJ.objects.all()
        context['courses'] = Course.objects.all()
        paginator = NamePaginator(self.object_list, on="last_name", per_page=12)
        try:
            page = int(self.request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            page = paginator.page(page)
        except (InvalidPage):
            page = paginator.page(paginator.num_pages)
        context['page'] = page
        return context

    @method_decorator(permission_required('is_staff'))
    def dispatch(self, *args, **kwargs):
        return super(UsersView, self).dispatch(*args, **kwargs)


class UserLoginView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(self.request, user)
        return redirect('teleforma-desk')

    @method_decorator(permission_required('is_staff'))
    def dispatch(self, *args, **kwargs):
        return super(UserLoginView, self).dispatch(*args, **kwargs)


class UsersTrainingView(UsersView):

    def get_queryset(self):
        self.training = Training.objects.filter(id=self.args[0])
        return User.objects.filter(student__training__in=self.training).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersTrainingView, self).get_context_data(**kwargs)
        context['training'] = Training.objects.get(id=self.args[0])
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersTrainingView, self).dispatch(*args, **kwargs)

class UsersIejView(UsersView):

    def get_queryset(self):
        self.iej = IEJ.objects.filter(id=self.args[0])
        return User.objects.filter(student__iej__in=self.iej).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersIejView, self).get_context_data(**kwargs)
        context['iej'] = IEJ.objects.get(id=self.args[0])
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersIejView, self).dispatch(*args, **kwargs)

class UsersCourseView(UsersView):

    def get_queryset(self):
        self.course = Course.objects.filter(id=self.args[0])
        return User.objects.filter(student__written_speciality__in=self.course)

    def get_context_data(self, **kwargs):
        context = super(UsersCourseView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.args[0])
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersCourseView, self).dispatch(*args, **kwargs)

def get_course_code(obj):
    if obj:
        return unicode(obj.code)
    else:
        return ''

class UsersXLSExport(object):

    first_row = 2

    def export_user(self, counter, user):
        student = Student.objects.filter(user=user)
        if student:
            student = Student.objects.get(user=user)
            row = self.sheet.row(counter + self.first_row)
            row.write(0, user.last_name)
            row.write(1, user.first_name)
            row.write(9, user.email)
            row.write(2, unicode(student.iej))
            code = student.training.code
            if student.platform_only:
                code = 'I - ' + code
            row.write(3, unicode(code))
            row.write(4, get_course_code(student.procedure))
            row.write(5, get_course_code(student.written_speciality))
            row.write(6, get_course_code(student.oral_speciality))
            row.write(7, get_course_code(student.oral_1))
            row.write(8, get_course_code(student.oral_2))

            profile = Profile.objects.filter(user=user)
            if profile:
                profile = Profile.objects.get(user=user)
                row.write(10, profile.address)
                row.write(11, profile.postal_code)
                row.write(12, profile.city)
                row.write(13, profile.telephone)
                row.write(14, user.date_joined.strftime("%d/%m/%Y"))
            return counter + 1
        else:
            return counter

    @method_decorator(permission_required('is_staff'))
    def export(self, request):
        self.users = self.users.order_by('last_name')
        self.book = Workbook()
        self.sheet = self.book.add_sheet('Etudiants')

        row = self.sheet.row(0)
        cols = [{'name':'NOM', 'width':5000},
                {'name':'PRENOM', 'width':5000},
                {'name':'IEJ', 'width':2500},
                {'name':'FORMATION', 'width':6000},
                {'name':'PROC', 'width':2500},
                {'name':'Ecrit Spe', 'width':3000},
                {'name':'Oral Spe', 'width':3000},
                {'name':'ORAL 1', 'width':3000},
                {'name':'ORAL 2', 'width':3000},
                {'name':'MAIL', 'width':7500},
                {'name':'ADRESSE', 'width':7500},
                {'name':'CP', 'width':2500},
                {'name':'VILLE', 'width':5000},
                {'name':'TEL', 'width':5000},
                {'name':"Date d'inscription", 'width':5000}
                ]
        i = 0
        for col in cols:
            row.write(i, col['name'])
            self.sheet.col(i).width = col['width']
            i += 1

        counter = 0
        for user in self.users:
            counter = self.export_user(counter, user)
        response = HttpResponse(mimetype="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        self.book.save(response)
        return response

    @method_decorator(permission_required('is_staff'))
    def all(self, request):
        self.users = User.objects.all()
        return self.export(request)

    @method_decorator(permission_required('is_staff'))
    def by_training(self, request, id):
        training = Training.objects.filter(id=id)
        self.users = User.objects.filter(student__training__in=training)
        return self.export(request)

    @method_decorator(permission_required('is_staff'))
    def by_iej(self, request, id):
        iej = IEJ.objects.filter(id=id)
        self.users = User.objects.filter(student__iej__in=iej)
        return self.export(request)

    @method_decorator(permission_required('is_staff'))
    def by_course(self, request, id):
        course = Course.objects.filter(id=id)
        self.users = User.objects.filter(student__training__courses__in=course)
        return self.export(request)


class HelpView(TemplateView):

    template_name='teleforma/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['page_content'] = pages.get_page_content(self.request, 'help',
                                                         ignore_slash_issue=True)
        return context

    def dispatch(self, *args, **kwargs):
        return super(HelpView, self).dispatch(*args, **kwargs)


