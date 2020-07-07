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
from django.core.exceptions import ValidationError, PermissionDenied
from teleforma.models.crfpa import Parameters
from teleforma.models.core import Period
from teleforma.views.core import *
from teleforma.forms import WriteForm
from telemeta.views import ProfileView
from registration.views import *
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from postman.views import WriteView as PostmanWriteView
from postman.forms import AnonymousWriteForm
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Max
from django.http import HttpResponseForbidden
from django.forms.formsets import all_valid
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site

ORAL_OPTION_PRICE = 250

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
        corrector_courses = set()
        for quota in quotas:
            corrector_courses.add(quota.course)
        for course in corrector_courses:
            courses = format_courses(courses, course=course,
                    types=CourseType.objects.all())

    elif student:
        student = user.student.get()
        if not student.trainings.all():
            return []
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
        if synthesis_note.count():
            courses = format_courses(courses,
                            queryset=Course.objects.filter(synthesis_note=True),
                            types=synthesis_note)

        obligation = training.obligation
        if obligation.count():
            courses = format_courses(courses,
                            queryset=Course.objects.filter(obligation=True),
                            types=obligation)

        magistral = training.magistral
        if magistral.count():
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

    if period:
        courses = [ c for c in courses if c['course'].is_for_period(period) ]

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
        old_last_login = user.last_login
        login(self.request, user)
        user.last_login = old_last_login
        user.save()
        return redirect('teleforma-home')

    @method_decorator(permission_required('is_staff'))
    def dispatch(self, *args, **kwargs):
        return super(UserLoginView, self).dispatch(*args, **kwargs)


class UserXLSBook(object):

    first_row = 2

    def __init__(self, students = None, users = None):
        self.book = Workbook()
        if students:
            self.students = students
        elif users:
            user_ids = [ u['id'] for u in users.values('id') ]
            self.students = Student.objects.filter(user_id__in = user_ids)
        else:
            self.students = []

        self.course_map = { c['id']: c['code'] for c in Course.objects.values('id', 'code') }

        self.sheet = self.book.add_sheet('Etudiants')

    def get_course_code(self, c_id):
        """
        Like get_course_code global but through the cache
        """
        return self.course_map.get(c_id, None) or ''

    def export_user(self, counter, student):
        # if counter >= 419:
        #     import pdb;pdb.set_trace()
        user = student.user
        if student.training:
            training = student.training
        elif student.trainings.all():
            training = student.trainings.all()[0]
        else:
            training = None
        if training:
            row = self.sheet.row(counter + self.first_row)
            row.write(0, user.last_name)
            row.write(1, user.first_name)
            row.write(2, student.portrait and student.portrait.url or '')
            row.write(8, user.email)
            row.write(3, unicode(student.iej))

            codes = []
            for training in student.trainings.values('code'):
                if student.platform_only:
                    codes.append('I - ' + training['code'])
                else:
                    codes.append(training['code'])
            row.write(4, unicode(' '.join(codes)))

            row.write(5, self.get_course_code(student.procedure_id))
            row.write(6, self.get_course_code(student.written_speciality_id))
            row.write(7, self.get_course_code(student.oral_1_id))

            profile = Profile.objects.filter(user=user)
            if profile:
                profile = profile[0]
                row.write(9, profile.address)
                row.write(10, profile.address_detail)
                row.write(11, profile.postal_code)
                row.write(12, profile.city)
                row.write(13, profile.telephone)
                if profile.birthday:
                    try:
                        row.write(14, profile.birthday.strftime("%d/%m/%Y"))
                    except ValueError:
                        row.write(14, 'erreur')

                row.write(15, student.level)

                if student.date_subscribed:
                    row.write(16, student.date_subscribed.strftime("%d/%m/%Y"))

            total_discount = 0
            descriptions = []
            for discount in student.discounts.values('value', 'description'):
                total_discount -= discount['value']
                descriptions.append(discount['description'])
            row.write(17, total_discount)
            row.write(18, ', '.join(descriptions))

            total_payments = 0
            payment_per_month = { month[0]: {'amount':0, 'type':set()} for month in months_choices }
            for payment in student.payments.values('month', 'value',
                                                   'type', 'online_paid'):
                if payment['type'] == 'online' and not payment['online_paid']:
                    continue
                value = payment['value']
                month = payment['month']
                ptype = payment['type']
                ptype_label = next((payment_choice[1] for payment_choice in payment_choices if payment_choice[0] == ptype), ['none'])
                total_payments += value
                if month in payment_per_month:
                    payment_per_month[month]['amount'] += value
                    payment_per_month[month]['type'].add(ptype_label)
                
            row.write(19, total_payments)

            row.write(20, student.total_fees)
            row.write(21, student.balance)
            row.write(22, student.total_paybacks)

            row.write(23, student.subscription_fees)
            row.write(24, student.fascicule)
                
            
            i = 25
            for month in months_choices:
                row.write(i, payment_per_month[month[0]]['amount'])
                row.write(i+1, ','.join(payment_per_month[month[0]]['type']))
                i += 2

            return counter + 1
        return counter

    def write(self):
        row = self.sheet.row(0)
        cols = [{'name':'NOM', 'width':5000},
                {'name':'PRENOM', 'width':5000},
                {'name': 'PHOTO', 'width': 7500},
                {'name':'IEJ', 'width':2500},
                {'name':'FORMATIONS', 'width':6000},
                {'name':'PROC', 'width':2500},
                {'name':'Ecrit Spe', 'width':3000},
                {'name':'ORAL 1', 'width':3000},
                {'name':'MAIL', 'width':7500},
                {'name':'ADRESSE', 'width':7500},
                {'name':'ADRESSE (suite)', 'width': 7500},
                {'name':'CP', 'width':2500},
                {'name':'VILLE', 'width':5000},
                {'name':'TEL', 'width':5000},
                {'name': 'Date de naissance', 'width': 5000},
                {'name': "Niveau d'etude", 'width': 5000},
                {'name':"Date inscription", 'width':5000},
                {'name':"Total reductions", 'width':4000},
                {'name':"Description reduction", 'width':4000},
                {'name':"Total paiements", 'width':4000},
                {'name':"Prix formation net", 'width':4000},
                {'name':"Balance", 'width':4000},
                {'name':"Total remboursement", 'width':4000},
                {'name': "Frais d'inscription", 'width': 4000},
                {'name':"Envoi des fascicules", 'width':3500},
                ]

        for month in months_choices:
            cols.append({'name': 'Paiement ' + slugify(month[1]), 'width': 4000})
            cols.append({'name': 'Type paiement ' + slugify(month[1]), 'width': 4000})

        i = 0
        for col in cols:
            row.write(i, col['name'])
            self.sheet.col(i).width = col['width']
            i += 1

        counter = 0
        for student in self.students:
            counter = self.export_user(counter, student)


class UsersExportView(UsersView):

    @method_decorator(permission_required('is_staff'))
    def get(self, *args, **kwargs):
        super(UsersExportView, self).get(*args, **kwargs)
        book = UserXLSBook(users = self.users)
        book.write()
        response = HttpResponse(mimetype="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        book.book.save(response)
        return response


class CorrectorXLSBook(object):

    first_row = 2

    def __init__(self, correctors):
        self.book = Workbook()
        self.correctors = correctors
        self.sheet = self.book.add_sheet('Correcteurs')

    def export_user(self, counter, corrector):
        # if counter >= 419:
        #     import pdb;pdb.set_trace()
        user = corrector.user
        row = self.sheet.row(counter + self.first_row)
        row.write(0, user.last_name)
        row.write(1, user.first_name)
        row.write(2, user.username)
        row.write(3, user.email)

        profile = Profile.objects.filter(user=user)
        if profile:
            profile = profile[0]
            row.write(4, profile.address)
            row.write(5, profile.address_detail)
            row.write(6, profile.postal_code)
            row.write(7, profile.city)
            row.write(8, profile.telephone)
            if profile.birthday:
                try:
                    row.write(9, profile.birthday.strftime("%d/%m/%Y"))
                except ValueError:
                    row.write(9, 'erreur')
            row.write(10, profile.birthday_place)
            row.write(11, profile.nationality)
            row.write(12, profile.ss_number)

            if corrector.date_registered:
                row.write(13, corrector.date_registered.strftime("%d/%m/%Y"))
            else:
                row.write(13, "")
            row.write(14, str(corrector.period))
            row.write(15, corrector.pay_status)
                
        return counter + 1

    def write(self):
        row = self.sheet.row(0)
        cols = [{'name':'NOM', 'width':5000},
                {'name':'PRENOM', 'width':5000},
                {'name':'ID', 'width':5000},
                {'name':'MAIL', 'width':7500},
                {'name':'ADRESSE', 'width':7500},
                {'name':'ADRESSE (suite)', 'width': 7500},
                {'name':'CP', 'width':2500},
                {'name':'VILLE', 'width':5000},
                {'name':'TEL', 'width':5000},
                {'name': 'DATE DE NAISSANCE', 'width': 5000},
                {'name': 'LIEU DE NAISSANCE', 'width': 5000},
                {'name': 'NATIONALITE', 'width': 5000},
                {'name': 'NUMERO SS', 'width': 5000},
                {'name':"DATE D'INSCRIPTION", 'width':5000},
                {'name':"PERIODE", 'width':5000},
                {'name':"STATUT", 'width':5000},
                ]
        
        i = 0
        for col in cols:
            row.write(i, col['name'])
            self.sheet.col(i).width = col['width']
            i += 1
            
        counter = 0
        for corrector in self.correctors:
            counter = self.export_user(counter, corrector)


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
            docs = Document.objects.filter(is_annal=True).filter(Q(iej=self.student.iej) | Q(iej=None)).order_by('-annal_year')
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


class UserAddView(CreateView):

    model = User
    template_name = 'registration/registration_form.html'
    form_class = UserForm
    # inlines = [ProfileInline, StudentInline]

    def get_context_data(self, **kwargs):
        context = super(UserAddView, self).get_context_data(**kwargs)
        parameters = Parameters.load()
        context['introduction'] = parameters.inscription_text
        return context

    def get_success_url(self):
        return reverse_lazy('teleforma-register-complete', kwargs={'username':self.object.username})

class UserCompleteView(TemplateView):

    template_name = 'registration/registration_complete.html'

    def get_context_data(self, **kwargs):
        context = super(UserCompleteView, self).get_context_data(**kwargs)
        # context['register_doc_print'] = Document.objects.get(id=settings.TELEFORMA_REGISTER_DEFAULT_DOC_ID)
        context['username'] = kwargs['username']
        user = User.objects.get(username=kwargs['username'])
        student = user.student.all()[0]
        context['period'] = student.period
        return context


class RegistrationPDFView(PDFTemplateResponseMixin, TemplateView):

    template_name = 'registration/registration_pdf.html'
    pdf_template_name = template_name

    def is_pdf(self):
        return True

    def get_context_data(self, **kwargs):
        context = super(RegistrationPDFView, self).get_context_data(**kwargs)
        user = User.objects.get(username=kwargs['username'])

        # some form fixes
        student = user.student.all()[0]
        if student.training and not student.trainings.all():
            student.trainings.add(student.training)
        if not student.training and student.trainings.all():
            student.training = student.trainings.all()[0]
        if not student.oral_1:
            student.oral_1 = Course.objects.get(code='X')
        if not student.oral_2:
            student.oral_2 = Course.objects.get(code='X')
        student.save()            
        profile = user.profile.all()[0]
        if profile.city:
            profile.city = profile.city.upper()
        if profile.country:
            profile.country = profile.country.upper()
        profile.save()

        context['student'] = student
        return context

class RegistrationPDFViewDownload(RegistrationPDFView):

    pdf_filename = 'registration.pdf'

    def get_pdf_filename(self):
        super(RegistrationPDFViewDownload, self).get_pdf_filename()
        user = User.objects.get(username=self.kwargs['username'])
        # user = self.get_object()
        student = user.student.all()[0]
        prefix = unicode(_('Registration'))
        filename = '_'.join([prefix, student.user.first_name, student.user.last_name])
        filename += '.pdf'
        return filename.encode('utf-8')

    
class ReceiptPDFView(PDFTemplateResponseMixin, TemplateView):

    template_name = 'receipt/receipt_pdf.html'
    pdf_template_name = template_name

    def get_context_data(self, **kwargs):
        context = super(ReceiptPDFView, self).get_context_data(**kwargs)
        user = User.objects.get(username=kwargs['username'])

        cur_user = self.request.user
        if not cur_user.is_authenticated():
            raise PermissionDenied
        if cur_user.pk != user.pk and not cur_user.is_superuser:
            raise PermissionDenied

        context['site'] = Site.objects.get_current()
        
        student = user.student.all()[0]

        if not student.training and student.trainings.all():
            student.training = student.trainings.all()[0]
        training = student.training
        period = training.period
        student.save()            
        profile = user.profile.all()[0]

        context['student'] = student
        context['profile'] = profile

        receipt_id = student.receipt_id
        if receipt_id is None:
            last = Student.objects.aggregate(Max('receipt_id'))
            last = last['receipt_id__max']
            if not last:
                last = 0
            receipt_id = last + 1
            student.receipt_id = receipt_id
            student.save()

        period_name = period.name.split()
        period_name = period_name[0].upper()
        context['receipt_id'] = "%s_%04d_%05d" % (period_name,
                                                  period.date_begin.year,
                                                  receipt_id)
        self.receipt_id = context['receipt_id']

        # Added items to pay
        items = []
        if student.application_fees:
            substract = student.default_application_fees
            items.append({ 'label': "<b>Frais de dossier</b>",
                           'unit_price': substract,
                           'amount': 1,
                           'discount': None, },)
        else:
            substract = 0

        label = u"<b>Préparation à l'examen du CRFPA</b><br/>"
        label += u"<b>%s &mdash; %s</b><br />" % (period, training.name)
        label += u"<i>%d heures de formation du %s au %s</i>" % (training.duration,
                                                                period.date_begin.strftime('%d/%m/%Y'),
                                                                period.date_end.strftime('%d/%m/%Y'),)

        oral_1 = student.oral_1 and student.oral_1.title != 'Aucune'
        
        if oral_1:
            substract += ORAL_OPTION_PRICE            
        
        items.append({ 'label': label,
                       'unit_price': student.total_fees - substract - student.total_discount,
                       'amount': 1,
                       'discount': student.total_discount, }, )
        if oral_1:
            items.append({ 'label': "<b>Option langue</b>",
                           'unit_price': ORAL_OPTION_PRICE,
                           'amount': 1,
                           'discount': 0, }, )
        for item in items:
            item['total'] = item['unit_price'] * item['amount']
            if item['discount']:
                item['total'] += item['discount']

        # Add payments
        payments = Payment.objects.filter(student = student)
        receipt_last = receipt_date = student.date_subscribed.date()
        for payment in payments:
            date = payment.scheduled or payment.date_modified.date()
            receipt_last = max(date, receipt_last)
            if payment.type == "online" and not payment.online_paid:
                continue
            receipt_date = max(date, receipt_date)
            date = date.strftime('%d/%m/%Y')
            kind = payment.get_type_display()
            items.append({ 'label': '<b>Paiement %s du %s</b>' % (kind, date),
                           'unit_price': None,
                           'amount': None,
                           'discount': None,
                           'total': -payment.value })

        context['receipt_date'] = receipt_date.strftime('%d/%m/%Y')
        context['receipt_last'] = receipt_last.strftime('%d/%m/%Y')

        context['receipt_items'] = items
        context['receipt_total'] = sum([ i['total'] for i in items ])
        return context
    
class ReceiptPDFViewDownload(ReceiptPDFView):

    pdf_filename = 'facture.pdf'

    def is_pdf(self):
        return True

    def get_pdf_filename(self):
        super(ReceiptPDFViewDownload, self).get_pdf_filename()
        user = User.objects.get(username=self.kwargs['username'])
        student = user.student.all()[0]
        prefix = "crfpa_facture"
        filename = '_'.join([prefix, self.receipt_id, student.user.first_name, student.user.last_name])
        filename += '.pdf'
        return filename.encode('utf-8')

    
class CorrectorRegistrationPDFView(PDFTemplateResponseMixin, TemplateView):

    template_name = 'registration/registration_corrector_pdf.html'
    pdf_template_name = template_name

    def is_pdf(self):
        return True

    def get_context_data(self, **kwargs):
        context = super(CorrectorRegistrationPDFView, self).get_context_data(**kwargs)
        user = User.objects.get(username=kwargs['username'])

        # some form fixes
        corrector = user.corrector.all()[0]
        profile = user.profile.all()[0]
        if profile.city:
            profile.city = profile.city.upper()
        if profile.country:
            profile.country = profile.country.upper()
        profile.save()

        context['corrector'] = corrector
        context['profile'] = profile
        return context
    
class RegistrationPDFViewDownload(RegistrationPDFView):

    pdf_filename = 'registration.pdf'

    def get_pdf_filename(self):
        super(RegistrationPDFViewDownload, self).get_pdf_filename()
        user = User.objects.get(username=self.kwargs['username'])
        # user = self.get_object()
        student = user.student.all()[0]
        prefix = unicode(_('Registration'))
        filename = '_'.join([prefix, student.user.first_name, student.user.last_name])
        filename += '.pdf'
        return filename.encode('utf-8')

class CorrectorRegistrationPDFViewDownload(RegistrationPDFView):

    pdf_filename = 'registration.pdf'

    def get_pdf_filename(self):
        super(RegistrationPDFViewDownload, self).get_pdf_filename()
        user = User.objects.get(username=self.kwargs['username'])
        # user = self.get_object()
        corrector = user.corrector.all()[0]
        prefix = unicode(_('Registration'))
        filename = '_'.join([prefix, corrector.user.first_name, corrector.user.last_name])
        filename += '.pdf'
        return filename.encode('utf-8')
    

class CorrectorAddView(CreateView):

    model = User
    template_name = 'registration/registration_form.html'
    form_class = CorrectorForm
    # inlines = [ProfileInline, StudentInline]

    def get_context_data(self, **kwargs):
        context = super(CorrectorAddView, self).get_context_data(**kwargs)
        parameters = Parameters.load()
        # context['introduction'] = parameters.inscription_text
        context['mode_corrector'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('teleforma-corrector-register-complete', kwargs={'username':self.object.username})
    
class CorrectorCompleteView(TemplateView):

    template_name = 'registration/registration_corrector_complete.html'

    def get_context_data(self, **kwargs):
        context = super(CorrectorCompleteView, self).get_context_data(**kwargs)
        # context['register_doc_print'] = Document.objects.get(id=settings.TELEFORMA_REGISTER_DEFAULT_DOC_ID)
        context['username'] = kwargs['username']
        user = User.objects.get(username=kwargs['username'])
        corrector = user.corrector.all()[0]
        context['period'] = corrector.period
        return context


@csrf_exempt
def update_training(request, id):
    platform_only = request.POST.get('platform_only', "") == 'True' and True or False
    trainings = Training.objects.filter(period__id=id, platform_only=platform_only)
    training_id = request.POST.get("training_id", "")

    html = '<option value="" selected="selected">---------</option>'
    for training in trainings:
        if training_id == str(training.pk):
            html+='<option value="%s" selected="selected">%s</option>' % (training.pk, training)
        else:
            html+='<option value="%s">%s</option>' % (training.pk, training)
    return HttpResponse(html)


class NewsItemMixin:
    model = NewsItem
    form_class = NewsItemForm
    def get_success_url(self):
        return reverse('teleforma-desk-period-course',
            kwargs={
            'pk': self.object.course.id,
            'period_id': self.request.GET.get('period_id')
            })

class NewsItemCreate(NewsItemMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.professor.count():
            return HttpResponseForbidden()
        return super(NewsItemCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        course_id = self.request.GET.get('course_id')
        course = None
        if course_id:
            course = get_object_or_404(Course, id=course_id)
        period_id = self.request.GET.get('period_id')
        period = None
        if period_id:
            period = get_object_or_404(Period, id=period_id)
        return {
            'course':course,
            'period':period
        }

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(NewsItemCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('teleforma-desk-period-course',
            kwargs={
            'pk': self.object.course.id,
            'period_id': self.request.GET.get('period_id')
            })

class NewsItemUpdate(NewsItemMixin, UpdateView):

    def form_valid(self, form):
        if not self.get_object().can_edit(self.request):
            return HttpResponseForbidden()
        return super(NewsItemUpdate, self).form_valid(form)

class NewsItemDelete(NewsItemMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        """
        """
        self.object = self.get_object()
        if not self.object.can_delete(request):
            return HttpResponseForbidden()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NewsItemList(ListView):

    model = NewsItem
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NewsItemList, self).get_context_data(**kwargs)
        context['course_id'] = self.request.GET.get('course_id', '')
        context['period_id'] = self.kwargs['period_id']
        return context

    def get_queryset(self):
        query = NewsItem.objects.filter(deleted=False, period__id=self.kwargs['period_id'])
        course_id = self.request.GET.get('course_id')
        if course_id:
            query = query.filter(course__id=self.request.GET.get('course_id'))
        return query


class WriteView(PostmanWriteView):
    """
    Display a form to compose a message.

    Optional URLconf name-based argument:
        ``recipients``: a colon-separated list of usernames
    Optional attributes:
        ``form_classes``: a 2-tuple of form classes
        ``autocomplete_channels``: a channel name or a 2-tuple of names
        ``template_name``: the name of the template to use
        + those of ComposeMixin

    """
    form_classes = (WriteForm, AnonymousWriteForm)
    success_url = "postman_sent"

class CRFPAProfileView(ProfileView):
    """Provide Collections web UI methods"""

    @method_decorator(login_required)
    def profile_detail(self, request, username, template='telemeta/profile_detail.html'):
        user = User.objects.get(username=username)
        try:
            profile = user.get_profile()
        except:
            profile = None
        playlists = get_playlists(request, user)
        user_revisions = get_revisions(25, user)
        student = user.student.all()
        payment = None
        if student and (user.username == request.user.username or request.user.is_superuser):
            student = user.student.get()
            payment = student.payments.order_by('-id').all()
            if payment:
                payment = payment[0]

        return render(request, template, {'profile' : profile, 'usr': user, 'playlists': playlists, 'payment':payment,
                                          'user_revisions': user_revisions})
