# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import View

from ..models.appointment import (CACHE_KEY, Appointment, AppointmentPeriod,
                                  AppointmentSlot)
from ..views.core import get_periods


class Appointments(View):
    template_name = 'teleforma/appointments.html'

    def check_rights(self, user, period_id):
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse('teleforma-login'))
        student = user.student.all().count()
        if not student:
            return HttpResponse('Unauthorized', status=401)
        period_id = int(period_id)
        periods = [ p for p in get_periods(self.request) if int(p.id) == period_id ]
        if not periods:
            return HttpResponse('Unauthorized', status=401)
        return

    def render(self, request, period_id, course_id):
        # Ensure user is logged in, a student, and has access to current period
        user = request.user

        # Get info
        ap_periods = []
        platform_only = user.student.get().platform_only
        for ap_period in AppointmentPeriod.objects.filter(periods__id=period_id, course_id=course_id).order_by('id'):
            if ap_period.is_open:
                modes = ap_period.modes
                # platformonly student can't subscribe to presentiel appointments
                # if platform_only:
                #     try:
                #         modes.remove(('presentiel', 'Presentiel'))
                #     except KeyError:
                #         pass
                ap_periods.append({
                    'days':ap_period.days(platform_only),
                    'name': ap_period.name,
                    'appointment':ap_period.get_appointment(user),
                    'modes':modes,
                    'course': ap_period.course,
                    'show_modes':len(ap_period.modes) > 1
                })
        # for ap_period in ap_periods:
        #     appointments[ap_period.id] = ap_period.get_appointments(request.user)

        return render(request, self.template_name, {'ap_periods': ap_periods, 'period_id':period_id})

    def check_validity(self, user, slot_id, slot_nb, jury_id):
        """
        Check if we can register to this exact slot
        """
        slot = get_object_or_404(AppointmentSlot, id = slot_id)

        # Check the period is open and
        if not slot.appointment_period.is_open:
            return u"La période de prise de rendez-vous est fermé."
        # Check  we are least delay (ie, 48h) before the date
        if not slot.can_book_today:
            delay = slot.appointment_period.book_delay
            return u"Vous devez réserver au moins %d jours ouvrés à l'avance" % delay
        # Check if this jury is open
        jurys = slot.get_visible_jurys
        if not jury_id in [ j.id for j in jurys ]:
            return u"Ce jury n'est pas ouvert"
        # Check if this slot is empty
        if Appointment.objects.filter(slot_id = slot_id, slot_nb = slot_nb,
                                      jury_id = jury_id).exists():
            return u"Ce créneau n'est plus disponible"
        # Check if this slot exists
        slot = get_object_or_404(AppointmentSlot, id = slot_id)
        if slot_nb >= slot.nb:
            return u"Ce créneau n'existe pas"
        # Check we don't have another appointment on this period
        if slot.appointment_period.get_appointment(user):
            return u"Vous avez déjà un rendez-vous"

    def post(self, request, period_id, course_id):

        user = request.user
        rights = self.check_rights(user, period_id)
        if rights:
            return rights

        slot_nb = int(request.POST.get('slot_nb'))
        slot_id = int(request.POST.get('slot'))
        jury_id = int(request.POST.get('jury'))

        msg = self.check_validity(user, slot_id, slot_nb, jury_id)

        if not msg:
            ap = Appointment()
            ap.slot_nb = slot_nb
            ap.slot_id = slot_id
            ap.jury_id = jury_id
            ap.student = user
            try:
                ap.save()
                cache.delete('%s_%s_%s-%s-True' % (CACHE_KEY, ap.slot.appointment_period.id, ap.slot.date, ap.slot.mode))
                cache.delete('%s_%s_%s-%s-None' % (CACHE_KEY, ap.slot.appointment_period.id, ap.slot.date, ap.slot.mode))
                cache.delete('%s_%s_%s-%s-False' % (CACHE_KEY, ap.slot.appointment_period.id, ap.slot.date, ap.slot.mode))
                self.send_ap_mail(ap)
            except IntegrityError:
                # Duplicate appointment caught by the db
                msg = u"Ce créneau n'est plus disponible"
            messages.add_message(request, messages.INFO, "Votre réservation a bien été prise en compte.")
        else:
            messages.add_message(request, messages.ERROR, msg)
        return self.render(request, period_id, course_id)

    def get(self, request, period_id, course_id):
        rights = self.check_rights(request.user, period_id)
        if rights:
            return rights
        return self.render(request, period_id, course_id)

    def send_ap_mail(self, ap):
        """
        Send the confirm mail to student
        """
        main_text = ap.slot.mode == 'distance' and ap.appointment_period.appointment_mail_text_distance or ap.appointment_period.appointment_mail_text
        data = { 'mfrom': settings.DEFAULT_FROM_EMAIL,
                 'mto': ap.student.email,
                 'title': ap.appointment_period.name,
                 'jury_address': ap.jury.address,
                 'arrival': ap.real_date,
                 'start': ap.start,
                 'end': ap.end,
                 'student': ap.student,
                 'mode': ap.slot.mode,
                 'bbb': ap.jury.bbb_room,
                 'main_text': main_text }
        # DEBUG
        # data['mto'] = "yoanl@pilotsystems.net"
        # data['mto'] = "dorothee.lavalle@pre-barreau.com"

        subject_template = 'teleforma/messages/email_appointment_sujet.txt'
        message_template = 'teleforma/messages/email_appointment.txt'
        subject = render_to_string(subject_template, data)
        subject = ''.join(subject.splitlines())
        message = render_to_string(message_template, data)
        send_mail(subject, message, data['mfrom'], [ data['mto'] ],
                  fail_silently=False)
        return data


def cancel_appointment(request):
    period_id = request.POST['period_id']
    course_id = request.POST['course_id']
    appointment_id = request.POST['appointment_id']

    app = get_object_or_404(Appointment, id=appointment_id)

    if app.student != request.user:
        return HttpResponse('Unauthorized', status=401)

    if not app.can_cancel():
        messages.add_message(request, messages.ERROR, 'Il est trop tard pour annuler ce rendez-vous.')
        return redirect('teleforma-appointments', period_id=period_id, course_id=course_id)

    cache.delete('%s_%s_%s-%s-True' % (CACHE_KEY, app.slot.appointment_period.id, app.slot.date, app.slot.mode))
    cache.delete('%s_%s_%s-%s-None' % (CACHE_KEY, app.slot.appointment_period.id, app.slot.date, app.slot.mode))
    cache.delete('%s_%s_%s-%s-False' % (CACHE_KEY, app.slot.appointment_period.id, app.slot.date, app.slot.mode))
    app.delete()
    messages.add_message(request, messages.INFO, 'Votre réservation a été annulé.')
    return redirect('teleforma-appointments', period_id=period_id, course_id=course_id)

