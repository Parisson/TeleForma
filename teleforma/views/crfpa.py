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


from teleforma.views.core import *


def get_crfpa_courses(user, date_order=False, num_order=False):
    courses = []

    if not user.is_authenticated():
        return courses

    professor = user.professor.all()
    student = user.crfpa_student.all()

    if professor:
        professor = user.professor.get()
        courses = format_courses(courses, queryset=professor.courses.all(),
                                  types=CourseType.objects.all())

    elif student:
        student = user.crfpa_student.get()
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
        return User.objects.filter(crfpa_student__training__in=self.training).order_by('last_name')

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
        return User.objects.filter(crfpa_student__iej__in=self.iej).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(UsersIejView, self).get_context_data(**kwargs)
        context['iej'] = IEJ.objects.get(id=self.args[0])
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersIejView, self).dispatch(*args, **kwargs)

class UsersCourseView(UsersView):

    def get_queryset(self):
        #TODO: optimize
        u = []
        self.course = Course.objects.get(id=self.args[0])
        users = User.objects.all()
        for user in users:
            user_courses = get_crfpa_courses(user)
            for course in user_courses:
                if course['course'] == self.course:
                    u.append(user)
        return u

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


class AnnalsView(ListView):

    model = Document
    template_name='teleforma/annals.html'
    student = None

    def get_docs(self, iej=None, course=None):
        students = self.user.crfpa_student.all()
        annals = {}
        courses = [c['course'] for c in self.all_courses]

        if self.user.is_staff or self.user.is_superuser or self.user.professor.all():
            docs = Document.objects.filter(is_annal=True).order_by('-annal_year')
        elif students:
            self.student = students[0]
            docs = Document.objects.filter(is_annal=True, iej=self.student.iej).order_by('-annal_year')
        if iej:
            docs = docs.filter(iej=iej)
        if course:
            print course
            docs = docs.filter(course=course)

        for doc in docs:
            if doc.course in courses:
                if not doc.course in annals.keys():
                    annals[doc.course] = {}
                if not doc.iej in annals[doc.course].keys():
                    annals[doc.course][doc.iej] = {}
                if not doc.annal_year in annals[doc.course][doc.iej].keys():
                    annals[doc.course][doc.iej][doc.annal_year] = []
                annals[doc.course][doc.iej][doc.annal_year].append(doc)
        return annals

    def get_queryset(self):
        self.user = self.request.user
        self.all_courses = get_courses(self.request.user)
        return self.get_docs()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(AnnalsView, self).get_context_data(**kwargs)
        context['iejs'] = IEJ.objects.all()
        if self.student:
            context['student'] =  self.student
        context['all_courses'] = self.all_courses
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnnalsView, self).dispatch(*args, **kwargs)


class AnnalsIEJView(AnnalsView):

    def get_queryset(self):
        self.user = self.request.user
        self.all_courses = get_courses(self.user)
        self.iej = IEJ.objects.filter(id=self.args[0])
        return self.get_docs(iej=self.iej)

class AnnalsCourseView(AnnalsView):

    def get_queryset(self):
        self.user = self.request.user
        self.all_courses = get_courses(self.user)
        self.course = Course.objects.filter(id=self.args[0])
        return self.get_docs(course=self.course)


