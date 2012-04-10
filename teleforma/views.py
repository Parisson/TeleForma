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

from teleforma.models import *
from telemeta.views.base import *
from jqchat.models import *



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


class CourseView(DetailView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['courses'] = get_courses(self.request.user)
        course = self.get_object()
        context['notes'] = course.notes.all().filter(author=self.request.user)
        return context

class CoursesView(ListView):

    model = Course
    template_name='teleforma/courses.html'

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['object_list'] = get_courses(self.request.user)
        context['notes'] = Note.objects.filter(author=self.request.user)
        return context

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
        context['room'] = media.course.chat_room
        return context

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
        return context

class UsersTrainingView(UsersView):

    def get_queryset(self):
        users = User.objects.all().select_related(depth=2)
        trainings = Training.objects.filter(id=self.args[0])
        return User.objects.filter(student__training__in=trainings)

