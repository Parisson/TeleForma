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

from django.contrib.auth import get_backends, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.paginator import InvalidPage
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.list import ListView
from teleforma.models.core import Course, CourseType, NamePaginator
from teleforma.models.crfpa import IEJ, Training


def format_crfpa_courses(courses, course=None, queryset=None, types=None, admin=False):
    if queryset:
        for c in queryset:
            if c and (c.code != 'X' or admin == True):
                courses.append({'course': c, 'types': types.all(),
                                'date': c.date_modified, 'number': c.number})
    elif course:
        if course.code != 'X' or admin == True:
            courses.append({'course': course, 'types': types.all(),
                            'date': course.date_modified, 'number': course.number})
    return courses


def get_crfpa_courses(user, date_order=False, num_order=False):
    courses = []

    if not user.is_authenticated:
        return courses

    professor = user.professor.all()
    student = user.student.all()

    if professor:
        professor = user.professor.get()
        courses = format_crfpa_courses(courses, queryset=professor.courses.all(),
                                       types=CourseType.objects.all())

    elif student:
        student = user.student.get()
        s_courses = {student.procedure: student.training.procedure,
                     student.written_speciality: student.training.written_speciality,
                     student.oral_speciality: student.training.oral_speciality,
                     student.oral_1: student.training.oral_1,
                     student.oral_2: student.training.oral_2,
                     student.options: student.training.options,
                     }

        for course in s_courses:
            courses = format_crfpa_courses(courses, course=course,
                                           types=s_courses[course])

        synthesis_note = student.training.synthesis_note
        if synthesis_note:
            courses = format_crfpa_courses(courses,
                                           queryset=Course.objects.filter(
                                               synthesis_note=True),
                                           types=synthesis_note)

        obligation = student.training.obligation
        if obligation:
            courses = format_crfpa_courses(courses,
                                           queryset=Course.objects.filter(
                                               obligation=True),
                                           types=obligation)

        magistral = student.training.magistral
        if magistral:
            courses = format_crfpa_courses(courses,
                                           queryset=Course.objects.filter(
                                               magistral=True),
                                           types=magistral)

    elif user.is_staff or user.is_superuser:
        courses = format_crfpa_courses(courses, queryset=Course.objects.all(),
                                       types=CourseType.objects, admin=True)
    else:
        courses = None

    if date_order:
        courses = sorted(courses, key=lambda k: k['date'], reverse=True)
    if num_order:
        courses = sorted(courses, key=lambda k: k['number'])

    return courses


class UsersView(ListView):

    model = User
    template_name = 'teleforma/users.html'
    context_object_name = 'users'
    #paginate_by = 12

    def get_queryset(self):
        return User.objects.all().select_related().order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        context['trainings'] = Training.objects.all()
        context['iejs'] = IEJ.objects.all()
        context['courses'] = Course.objects.all()
        paginator = NamePaginator(
            self.object_list, on="last_name", per_page=10)
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
        user.backend = "%s.%s" % (
            backend.__module__, backend.__class__.__name__)
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
        return str(obj.code)
    else:
        return ''
