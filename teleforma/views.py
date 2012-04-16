# Create your views here.

import mimetypes

from jsonrpc import jsonrpc_method

from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
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
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from teleforma.models import *
from telemeta.views.base import *
import jqchat.models
from xlwt import Workbook



def render(request, template, data = None, mimetype = None):
    return render_to_response(template, data, context_instance=RequestContext(request),
                              mimetype=mimetype)

def get_courses(user):
    professor = user.professor.all()
    student = user.student.all()
    if professor:
        courses = user.professor.get().courses.all()
    elif student:
        courses = user.student.get().training.courses.all()
    elif user.is_staff:
        courses = Course.objects.all()
    else:
        courses = None
    courses = courses.order_by('-date_modified')
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

def document_download(request, pk):
    document = Document.objects.get(id=pk)
    fsock = open(document.file.path, 'r')
    mimetype = mimetypes.guess_type(document.file.path)[0]
    extension = mimetypes.guess_extension(mimetype)
    response = HttpResponse(fsock, mimetype=mimetype)
    response['Content-Disposition'] = "attachment; filename=%s%s" % \
                                     (unicode(document), extension)
    return response

def document_view(request, pk):
    document = Document.objects.get(id=pk)
    fsock = open(document.file.path, 'r')
    mimetype = mimetypes.guess_type(document.file.path)[0]
    extension = mimetypes.guess_extension(mimetype)
    response = HttpResponse(fsock, mimetype=mimetype)
    return response

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


class CourseView(DetailView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['courses'] = get_courses(self.request.user)
        course = self.get_object()
        context['notes'] = course.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="course")
        context['room'] = get_room(name=course.title, content_type=content_type,
                                   id=course.id)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseView, self).dispatch(*args, **kwargs)


class CoursesView(ListView):

    model = Course
    template_name='teleforma/courses.html'

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['object_list'] = get_courses(self.request.user)
        context['notes'] = Note.objects.filter(author=self.request.user)
        context['room'] = get_room(name='site')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CoursesView, self).dispatch(*args, **kwargs)


class MediaView(DetailView):

    model = Media
    template_name='teleforma/course_media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaView, self).get_context_data(**kwargs)
        context['courses'] = get_courses(self.request.user)
        media = self.get_object()
        view = ItemView()
        context['mime_type'] = view.item_analyze(media.item)
        context['course'] = media.course
        context['item'] = media.item
        context['notes'] = media.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="media")
        context['room'] = get_room(name=media.item.title, content_type=content_type,
                                   id=media.id)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaView, self).dispatch(*args, **kwargs)


class UsersView(ListView):

    model = User
    template_name='telemeta/users.html'
    context_object_name = 'users'
    paginate_by = 12

    def get_queryset(self):
        return User.objects.all().select_related(depth=1).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        context['trainings'] = Training.objects.all()
        context['all_users'] = User.objects.all()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersView, self).dispatch(*args, **kwargs)


class UsersTrainingView(UsersView):

    def get_queryset(self):
        self.trainings = Training.objects.filter(id=self.args[0])
        return User.objects.filter(student__training__in=self.trainings).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersTrainingView, self).get_context_data(**kwargs)
        context['training'] = Training.objects.get(id=self.args[0])
        context['all_users'] = User.objects.filter(student__training__in=self.trainings).all()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersTrainingView, self).dispatch(*args, **kwargs)


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
            row.write(3, unicode(student.training.code))
            row.write(4, unicode(student.procedure))
            row.write(5, unicode(student.written_speciality))
            row.write(6, unicode(student.oral_speciality))
            row.write(7, unicode(student.oral_1))
            row.write(8, unicode(student.oral_2))

            profile = Profile.objects.filter(user=user)
            if profile:
                profile = Profile.objects.get(user=user)
                row.write(10, profile.address)
                row.write(11, profile.postal_code)
                row.write(12, profile.city)
                row.write(13, profile.telephone)
                row.write(14, profile.date_added.strftime("%d/%m/%Y"))
            return counter + 1
        else:
            return counter

    @method_decorator(permission_required('is_superuser'))
    def export(self, request):
        self.book = Workbook()
        self.sheet = self.book.add_sheet('Etudiants')
        row = self.sheet.row(0)
        row.write(0, 'NOM')
        row.write(1, 'PRENOM')
        row.write(2, 'IEJ')
        row.write(3, 'FORMATION')
        row.write(4, 'PROC')
        row.write(5, 'Ecrit Spe')
        row.write(6, 'Oral Spe')
        row.write(7, 'ORAL 1')
        row.write(8, 'ORAL 2')
        row.write(9, 'MAIL')
        row.write(10, 'ADRESSE')
        row.write(11, 'CP')
        row.write(12, 'VILLE')
        row.write(13, 'TEL')
        row.write(14, "Date d'inscription")
        counter = 0
        for user in self.users:
            counter = self.export_user(counter, user)
        response = HttpResponse(mimetype="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        self.book.save(response)
        return response

    @method_decorator(permission_required('is_superuser'))
    def all(self, request):
        self.users = User.objects.all()
        return self.export(request)

    @method_decorator(permission_required('is_superuser'))
    def by_training(self, request, id):
        trainings = Training.objects.filter(id=id)
        self.users = User.objects.all().select_related(depth=2).filter(student__training__in=trainings)
        return self.export(request)
