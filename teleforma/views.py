# Create your views here.

import mimetypes

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
        professor = user.professor.get()
        courses = [{'courses': professor.courses.all(),
                    'types': CourseType.objects.all()},
                    ]
    elif student:
        student = user.student.get()

        courses =      [{'courses': student.procedure.all(),
                        'types':student.training.procedure.all()},
                        {'courses': student.written_speciality.all(),
                        'types':student.training.written_speciality.all()},
                        {'courses': student.oral_speciality.all(),
                        'types':student.training.oral_speciality.all()},
                        {'courses': student.oral_1.all(),
                        'types':student.training.oral_1.all()},
                        {'courses': student.oral_2.all(),
                        'types':student.training.oral_2.all()},
                        {'courses': student.options.all(),
                        'types':student.training.options.all()},
                        ]

        synthesis_note = student.training.synthesis_note.all()
        if synthesis_note:
            c = Course.objects.filter(synthesis_note=True)
            t = student.training.synthesis_note.all()
            courses.append({'courses': c, 'types': t})
        obligation = student.training.obligation.all()
        if obligation:
            c = Course.objects.filter(obligation=True)
            t = student.training.obligation.all()
            courses.append({'courses': c, 'types': t})

    elif user.is_staff:
        courses = [{'courses': Course.objects.all(),
                    'types': CourseType.objects.all()},
                   ]
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
                                     (unicode(document.title.decode('utf8')), extension)
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

    def get_queryset(self):
        return get_courses(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['courses'] = self.object_list
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


class DocumentView(DetailView):

    model = Document
    template_name='teleforma/course_document.html'

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['courses'] = get_courses(self.request.user)
        document = self.get_object()

#        context['mime_type'] = view.item_analyze(media.item)
        context['course'] = document.course
        context['notes'] = document.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="document")
        context['room'] = get_room(name=document.title, content_type=content_type,
                                   id=document.id)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DocumentView, self).dispatch(*args, **kwargs)

class ConferenceView(DetailView):

    model = Conference
    template_name='teleforma/course_conference.html'

    def get_context_data(self, **kwargs):
        context = super(ConferenceView, self).get_context_data(**kwargs)
        context['courses'] = get_courses(self.request.user)
        conference = self.get_object()
        context['mime_type'] = 'video/webm'
        context['course'] = conference.course
        context['notes'] = conference.notes.all().filter(author=self.request.user)
        content_type = ContentType.objects.get(app_label="teleforma", model="conference")
        context['room'] = get_room(name=conference.course.title, content_type=content_type,
                                   id=conference.id)
        context['livestream'] = conference.livestream.get().url
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConferenceView, self).dispatch(*args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersView, self).dispatch(*args, **kwargs)


class UserLoginView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(self.request, user)
        return redirect('teleforma-desk')

    @method_decorator(permission_required('is_superuser'))
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
        return User.objects.filter(student__training__courses__in=self.course)

    def get_context_data(self, **kwargs):
        context = super(UsersCourseView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.args[0])
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersCourseView, self).dispatch(*args, **kwargs)


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
                row.write(14, user.date_joined.strftime("%d/%m/%Y"))
            return counter + 1
        else:
            return counter

    @method_decorator(permission_required('is_superuser'))
    def export(self, request):
        self.users = self.users.order_by('last_name')
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
        training = Training.objects.filter(id=id)
        self.users = User.objects.filter(student__training__in=training)
        return self.export(request)

    @method_decorator(permission_required('is_superuser'))
    def by_iej(self, request, id):
        iej = IEJ.objects.filter(id=id)
        self.users = User.objects.filter(student__iej__in=iej)
        return self.export(request)

    @method_decorator(permission_required('is_superuser'))
    def by_course(self, request, id):
        course = Course.objects.filter(id=id)
        self.users = User.objects.filter(student__training__courses__in=course)
        return self.export(request)
