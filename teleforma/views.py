# Create your views here.

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

from teleforma.models import *

from telemeta.views.base import *


def render(request, template, data = None, mimetype = None):
    return render_to_response(template, data, context_instance=RequestContext(request),
                              mimetype=mimetype)


class CourseView(DetailView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['searches'] = Search.objects.filter(username=self.request.user)
        return context

class CoursesView(ListView):

    model = Course
    template_name='teleforma/courses.html'

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['searches'] = Search.objects.filter(username=self.request.user)
        return context

class MediaView(DetailView):

    model = Media
    template_name='teleforma/course_media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        media = self.get_object()
        view = ItemView()
        context['mime_type'] = view.item_analyze(media.item)
        context['course'] = media.course
        context['item'] = media.item
        context['searches'] = Search.objects.filter(username=self.request.user)
        return context
