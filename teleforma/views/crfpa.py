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
from registration.views import *
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from django.utils.translation import ugettext_lazy as _


def get_course_code(obj):
    if obj:
        return unicode(obj.code)
    else:
        return ''

def get_crfpa_courses(user, date_order=False, num_order=False, period=None):
    courses = []

    if not user.is_authenticated():
        return courses

    professor = user.professor.all()
    student = user.student.all()
    quotas = user.quotas.all()

    if professor:
        professor = user.professor.get()
        courses = format_courses(courses, queryset=professor.courses.all(),
                                  types=CourseType.objects.all())

    elif quotas and not user.is_staff:
        queryset = Course.objects.all()
        for quota in quotas:
            queryset = queryset.filter(quotas=quota)
        courses = format_courses(courses, queryset=queryset,
                    types=CourseType.objects.all())

    elif student:
        student = user.student.get()
        for training in student.trainings.all():
            if training.period == period:
                break

        s_courses = {student.procedure:training.procedure,
                           student.written_speciality:training.written_speciality,
                           student.oral_speciality:training.oral_speciality,
                           student.oral_1:training.oral_1,
                           student.oral_2:training.oral_2,
                           student.options:training.options,
                        }

        for course in s_courses:
            courses = format_courses(courses, course=course,
                               types=s_courses[course])

        synthesis_note = training.synthesis_note
        if synthesis_note:
            courses = format_courses(courses,
                            queryset=Course.objects.filter(synthesis_note=True),
                            types=synthesis_note)

        obligation = training.obligation
        if obligation:
            courses = format_courses(courses,
                            queryset=Course.objects.filter(obligation=True),
                            types=obligation)

        magistral = training.magistral
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
    training = None
    iej = None
    course = None
    #paginate_by = 12


    def get_queryset(self):
        self.users = User.objects.all().select_related(depth=1).order_by('last_name')

        if self.kwargs['training_id'] != '0':
            self.training = Training.objects.filter(id=self.kwargs['training_id'])
            self.users = self.users.filter(student__trainings__in=self.training)
            self.training = self.training[0]
        else:
            self.training = Training(id=0)

        if self.kwargs['iej_id'] != '0':
            self.iej = IEJ.objects.filter(id=self.kwargs['iej_id'])
            self.users = self.users.filter(student__iej__in=self.iej)
            self.iej = self.iej[0]
        else:
            self.iej = IEJ(id=0)

        if self.kwargs['course_id'] != '0':
            self.course = Course.objects.get(id=self.kwargs['course_id'])
            u = []
            for user in self.users:
                user_courses = get_crfpa_courses(user)
                for course in user_courses:
                    if course['course'] == self.course:
                        u.append(user)
            self.users = u
        else:
            self.course = Course(id=0)

        return self.users

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        users = self.object_list

        context['training'] = self.training
        context['iej'] = self.iej
        context['course'] = self.course

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
        return redirect('teleforma-home')

    @method_decorator(permission_required('is_staff'))
    def dispatch(self, *args, **kwargs):
        return super(UserLoginView, self).dispatch(*args, **kwargs)


class UserXLSBook(object):

    first_row = 2

    def __init__(self, users):
        self.book = Workbook()
        self.users = users
        self.sheet = self.book.add_sheet('Etudiants')

    def export_user(self, counter, user):
        student = Student.objects.filter(user=user)
        if student:
            student = Student.objects.get(user=user)
            row = self.sheet.row(counter + self.first_row)
            row.write(0, user.last_name)
            row.write(1, user.first_name)
            row.write(9, user.email)
            row.write(2, unicode(student.iej))

            codes = []
            for training in student.trainings.all():
                if student.platform_only:
                    codes.append('I - ' + training.code)
                else:
                    codes.append(training.code)
            row.write(3, unicode(' '.join(codes)))

            row.write(4, get_course_code(student.procedure))
            row.write(5, get_course_code(student.written_speciality))
            row.write(6, get_course_code(student.oral_speciality))
            row.write(7, get_course_code(student.oral_1))
            row.write(8, get_course_code(student.oral_2))

            profile = Profile.objects.filter(user=user)
            student = Student.objects.get(user=user)
            if profile:
                profile = Profile.objects.get(user=user)
                row.write(10, profile.address)
                row.write(11, profile.postal_code)
                row.write(12, profile.city)
                row.write(13, profile.telephone)
                if student.date_subscribed:
                    row.write(14, student.date_subscribed.strftime("%d/%m/%Y"))

            row.write(15, student.total_payments)
            row.write(16, student.total_fees)
            row.write(17, student.balance)

            payments = student.payments.all()
            i = 18
            for month in months_choices:
                payment = payments.filter(month=month[0])
                if payment:
                    value = payment[0].value
                else:
                    value = 0
                row.write(i, value)
                i += 1

            return counter + 1
        else:
            return counter

    def write(self):
        row = self.sheet.row(0)
        cols = [{'name':'NOM', 'width':5000},
                {'name':'PRENOM', 'width':5000},
                {'name':'IEJ', 'width':2500},
                {'name':'FORMATIONS', 'width':6000},
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
                {'name':"Date d'inscription", 'width':5000},
                {'name':"Total paiements", 'width':4000},
                {'name':"Total reductions", 'width':4000},
                {'name':"Balance", 'width':4000},
                ]
        for month in months_choices:
            cols.append({'name': 'Paiement ' + slugify(month[1]), 'width': 4000})

        i = 0
        for col in cols:
            row.write(i, col['name'])
            self.sheet.col(i).width = col['width']
            i += 1

        counter = 0
        for user in self.users:
            counter = self.export_user(counter, user)



class UsersExportView(UsersView):

    @method_decorator(permission_required('is_staff'))
    def get(self, *args, **kwargs):
        super(UsersExportView, self).get(*args, **kwargs)
        book = UserXLSBook(self.users)
        book.write()
        response = HttpResponse(mimetype="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        book.book.save(response)
        return response


class AnnalsView(ListView):

    model = Document
    template_name='teleforma/annals.html'
    student = None

    def get_docs(self, iej=None, course=None):
        students = self.user.student.all()
        annals = {}
        courses = [c['course'] for c in self.all_courses]

        if self.user.is_staff or self.user.is_superuser or self.user.professor.all() or self.user.quotas.all():
            docs = Document.objects.filter(is_annal=True).order_by('-annal_year')
        elif students:
            self.student = students[0]
            docs = Document.objects.filter(is_annal=True, iej=self.student.iej).order_by('-annal_year')
        if iej:
            docs = docs.filter(iej=iej)
        if course:
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
        periods = get_periods(user)
        context['period'] = periods[0]
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


def get_unique_username(first_name, last_name):
    username = slugify(first_name)[0] + '.' + slugify(last_name)
    username = username[:30]
    i = 1
    while User.objects.filter(username=username[:30]):
        username = slugify(first_name)[:i] + '.' + slugify(last_name)
        i += 1
    return username[:30]


class UserAddView(CreateWithInlinesView):

    model = User
    template_name = 'registration/registration_form.html'
    form_class = UserForm
    inlines = [ProfileInline, StudentInline]
    success_url = reverse_lazy('teleforma-register-complete')

    def forms_valid(self, form, inlines):
        messages.info(self.request, _("You have successfully register your account."))
        user = form.save()
        user.username = get_unique_username(user.first_name, user.last_name)
        user.is_active = False
        user.save()
        return super(UserAddView, self).forms_valid(form, inlines)


class UserCompleteView(TemplateView):

    template_name = 'registration/registration_complete.html'

    def get_context_data(self, **kwargs):
        context = super(UserCompleteView, self).get_context_data(**kwargs)
        context['register_doc_print'] = Document.objects.get(id=settings.TELEFORMA_REGISTER_DEFAULT_DOC_ID)
        return context
