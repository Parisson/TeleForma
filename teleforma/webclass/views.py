# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, View
from bigbluebutton_api_python.exception import BBBException

from datetime import datetime
import string
import random

from ..models.core import Conference, Course, Professor

from ..decorators import access_required
from ..views.core import get_courses, get_periods
from ..webclass.forms import WebclassRecordsForm
from ..webclass.models import BBBServer, Webclass, WebclassRecord, WebclassSlot
from django.contrib.auth.models import User


class WebclassProfessorAppointments(TemplateView):
    template_name = 'webclass/appointments_professor.html'

    def get_context_data(self, **kwargs):
        """ """
        context = super(WebclassProfessorAppointments,
                        self).get_context_data(**kwargs)

        user = self.request.user
        if not user.professor.all() and not user.is_superuser:
            return HttpResponse('Unauthorized', status=401)
        today = datetime.today()
        query = {
            'webclass__status': 3,
            'webclass__end_date__gte': today
        }
        if user.professor.all():
            query['professor'] = user.professor.get()
        context['slots'] = WebclassSlot.published.filter(**query).order_by('day', 'start_hour')
        context['is_superuser'] = user.is_superuser
        return context


class WebclassAppointment(View):
    template_name = 'webclass/appointments.html'

    def check_rights(self, user, webclass):
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse('teleforma-login'))
        student = user.student.all()[:1]
        if not student:
            return HttpResponse('Unauthorized', status=401)
        student = student[0]
        # check period
        period_id = webclass.period.id
        periods = [p for p in get_periods(self.request) if int(p.id) == period_id]
        if not periods:
            return HttpResponse('Unauthorized', status=401)
        # check courses
        course_id = webclass.course.id
        courses = [c for c in get_courses(
            user) if int(c['course'].id) == course_id]
        if not courses:
            return HttpResponse('Unauthorized', status=401)
        # Student is in the right IEJ ?
        if not student.iej in webclass.iej.all():
            return HttpResponse('Unauthorized', status=401)
        if student.platform_only and not webclass.allow_elearning:
            return HttpResponse('Unauthorized', status=401)
        if not student.platform_only and not webclass.allow_presentiel:
            return HttpResponse('Unauthorized', status=401)
            
        return

    def render(self, request, webclass):
        # Ensure user is logged in, a student, and has access to current period
        user = request.user
        student = user.student.all()[0]
        slots = webclass.slots.order_by('day', 'start_hour')
        # only display unavaible slots or first slot of the day
        filtered_slots = []
        day = None
        for slot in slots:
            if slot.participant_slot_available:
                if slot.day != day:
                    filtered_slots.append(slot)
                    day = slot.day
            else:
                filtered_slots.append(slot)

        return render(request, self.template_name, {'slots': filtered_slots, 'webclass': webclass})

    def check_slot_validity(self, user, slot):
        """
        Check if we can register to this exact slot
        """
        student = user.student.all()[0]

        # Check if there is still space for one student
        if not slot.participant_slot_available:
            return u"Ce créneau n'est plus disponible."

        # Check we don't have another appointment on this period
        webclass = slot.webclass
        if webclass.get_slot(user):
            return u"Vous êtes déjà inscrit."

    def post(self, request, pk):
        webclass = get_object_or_404(Webclass, id=pk)
        rights = self.check_rights(request.user, webclass)
        if rights:
            return rights

        user = request.user
        slot_id = int(request.POST.get('slot_id'))
        slot = WebclassSlot.published.get(pk=slot_id)

        msg = self.check_slot_validity(user, slot)

        if not msg:
            slot.participants.add(user)
            slot.save()
            # self.send_ap_mail(ap)
            messages.add_message(request, messages.INFO,
                                 "Votre réservation a bien été prise en compte.")
            return HttpResponseRedirect(reverse('teleforma-desk-period-course', kwargs={'period_id': webclass.period.id, 'pk': webclass.course.id}))
        else:
            messages.add_message(request, messages.ERROR, msg)
        return self.render(request, webclass)

    def get(self, request, pk):
        webclass = get_object_or_404(Webclass, id=pk)
        rights = self.check_rights(request.user, webclass)
        if rights:
            return rights
        return self.render(request, webclass)

    # def send_ap_mail(self, ap):
    #     """
    #     Send the confirm mail to student
    #     """
    #     data = { 'mfrom': settings.DEFAULT_FROM_EMAIL,
    #              'mto': ap.student.email,
    #              'jury_address': ap.jury.address,
    #              'date': ap.real_date,
    #              'student': ap.student,
    #              'main_text': ap.appointment_period.appointment_mail_text }
    #     # DEBUG
    #     # data['mto'] = "yoanl@pilotsystems.net"
    #     # data['mto'] = "dorothee.lavalle@pre-barreau.com"
    #     # data['mto'] = "gael@pilotsystems.net"

    #     subject_template = 'teleforma/messages/email_appointment_sujet.txt'
    #     message_template = 'teleforma/messages/email_appointment.txt'
    #     subject = render_to_string(subject_template, data)
    #     subject = ''.join(subject.splitlines())
    #     message = render_to_string(message_template, data)
    #     send_mail(subject, message, data['mfrom'], [ data['mto'] ],
    #               fail_silently=False)
    #     return data



class WebclassRecordView(TemplateView):
    template_name = 'webclass/record.html'

    def get_context_data(self, **kwargs):
        """ """
        context = super(WebclassRecordView, self).get_context_data(**kwargs)
        context['record_url'] = self.request.GET.get('url')
        return context


class WebclassRecordsFormView(FormView):
    template_name = 'webclass/records_form.html'
    form_class = WebclassRecordsForm
    success_url = '/admin/webclass/webclassrecord'

    def get_form_kwargs(self):
        kwargs = super(WebclassRecordsFormView, self).get_form_kwargs()
        kwargs['period_id'] = int(self.kwargs['period_id'])
        return kwargs

    def form_valid(self, form):
        form.save_records()
        return super(WebclassRecordsFormView, self).form_valid(form)

    @method_decorator(permission_required('is_superuser'))
    @method_decorator(access_required)
    def dispatch(self, *args, **kwargs):
        return super(WebclassRecordsFormView, self).dispatch(*args, **kwargs)


@access_required
def join_webclass(request, pk):
    webclass_slot = WebclassSlot.published.get(pk=int(pk))
    # webclass = webclass_slot.webclass
    # fake debug links
    # username = request.GET.get('username')
    # if username:
    #     return redirect(webclass.get_fake_join_webclass_url(request, username))
    user = request.user
    authorized = False

    # staff or professor ?
    is_professor = len(user.professor.all()) >= 1
    is_staff = user.is_staff or user.is_superuser
    if is_professor or is_staff:
        authorized = True

    # student registered ?
    if not authorized:
        if user in webclass_slot.participants.all():
            authorized = True

    if authorized:
        return redirect(webclass_slot.get_join_webclass_url(request, user))
    else:
        return HttpResponse('Unauthorized', status=401)


@access_required
def unregister(request, pk):
    """
    Unregister to a webclass
    """
    webclass_slot = WebclassSlot.objects.get(pk=int(pk))
    user = request.user

    if user in webclass_slot.participants.all():
        webclass_slot.participants.remove(user)

    messages.add_message(request, messages.INFO,
                                 "Votre réservation a été annulé.")
    # redirect to register form
    return redirect(reverse("teleforma-webclass-appointments", kwargs={'pk':webclass_slot.webclass.id}))



@access_required
def create_cc_bbb_conference(request, period_id, course_id):
    """
    Join a bbb webclass for "correction de copie" (cc) with a random room id. 
    A cron script will later create a WebclassRecord object.
    """

    username = request.user.get_full_name()
    is_professor = len(request.user.professor.all()) >= 1
    is_staff = request.user.is_staff or request.user.is_superuser

    if not is_professor and not is_staff:
        raise ValueError("User is not a professor or staff")
    course = Course.objects.get(pk=course_id)

    year = datetime.now().year
    bbb = BBBServer.objects.get(pk=2).get_instance()
    # generate password
    password = User.objects.make_random_password()
    # generate random room id
    room_id = "".join(random.choices(string.ascii_letters + string.digits, k=20))

    params = {
        'name': "Conférence %s" % course.title,
        'moderatorPW': password,
        'attendeePW': "PWATTENDEE",
        # 'maxParticipants':self.webclass_max_participants + 1,
        'welcome': "Pré-Barreau : Bienvenue sur la conférence \"%s\"." % (course.title),
        'record': True,
        'autoStartRecording':True,
        'muteOnStart': True,
        'allowModsToUnmuteUsers': True,
        'logo':'https://e-learning.crfpa.pre-barreau.com/static/teleforma/images/logo_pb.png',
        'copyright': "© %d Pré-Barreau" % year,
        # 'guestPolicy':'ALWAYS_ACCEPT'
        'bannerText': "Pré-Barreau - CRFPA",
        'bannerColor': "#003768",
        # 'customStyleUrl': site_url+"/static/teleforma/css/bbb.css"
        'logoutURL': "https://e-learning.ae.pre-barreau.com",
        'endWhenNoModerator': True,
        'meetingLayout': "VIDEO_FOCUS",
        "notifyRecordingIsOn": True,
    }

    meta = {
        'origin': 'crfpa',
        'periodid': period_id,
        'courseid': course_id,
        'professorid': request.user.id,
        'type': 'cc',
    }

    try:
        result = bbb.create_meeting(
            room_id, params=params, meta=meta)
    except BBBException as e:
        print(e)
        raise

    try:
        professor = request.user.professor.get()
    except Professor.DoesNotExist:
        professor = None

    WebclassRecord.objects.create(
        room_id=room_id,
        bbb_server=BBBServer.objects.get(pk=2),
        period_id=period_id,
        course_id=course_id,
        category=WebclassRecord.CORRECTION,
        professor=professor,
    )

    params = {'userID': request.user.username}
    return redirect(bbb.get_join_meeting_url(username, room_id, password, params))
