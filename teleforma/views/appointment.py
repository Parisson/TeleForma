# -*- coding: utf-8 -*-

from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings

from teleforma.models.appointment import AppointmentPeriod, Appointment, AppointmentSlot

from teleforma.views.core import get_periods


class Appointments(View):
    template_name = 'teleforma/appointments.html'

    def check_rights(self, user, period_id):
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('teleforma-login'))
        student = user.student.all().count()
        if not student:
            return HttpResponse('Unauthorized', status=401)
        period_id = int(period_id)
        periods = [ p for p in get_periods(user) if int(p.id) == period_id ]
        if not periods:
            return HttpResponse('Unauthorized', status=401)
        return

    def render(self, request, period_id):
        # Ensure user is logged in, a student, and has access to current period
        user = request.user

        # Get info
        ap_periods = []
        for ap_period in AppointmentPeriod.objects.filter(periods__id=period_id).order_by('id'):
            if ap_period.is_open:
                ap_periods.append({
                    'days':ap_period.days,
                    'name': ap_period.name,
                    'appointment':ap_period.get_appointment(user)
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

    def post(self, request, period_id):

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
                self.send_ap_mail(ap)
            except IntegrityError:
                # Duplicate appointment caught by the db
                msg = u"Ce créneau n'est plus disponible"
            messages.add_message(request, messages.INFO, "Votre réservation a bien été prise en compte.")
        else:
            messages.add_message(request, messages.ERROR, msg)
        return self.render(request, period_id)

    def get(self, request, period_id):
        rights = self.check_rights(request.user, period_id)
        if rights:
            return rights
        return self.render(request, period_id)

    def send_ap_mail(self, ap):
        """
        Send the confirm mail to student
        """
        data = { 'mfrom': settings.DEFAULT_FROM_EMAIL,
                 'mto': ap.student.email,
                 'jury_address': ap.jury.address,
                 'date': ap.real_date,
                 'student': ap.student,
                 'main_text': ap.appointment_period.appointment_mail_text }
        # DEBUG
        data['mto'] = "yoanl@pilotsystems.net"
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
    appointment_id = request.POST['appointment_id']

    app = get_object_or_404(Appointment, id=appointment_id)

    if app.student != request.user:
        return HttpResponse('Unauthorized', status=401)

    if not app.can_cancel():
        messages.add_message(request, messages.ERROR, 'Il est trop tard pour annuler ce rendez-vous.')
        return redirect('teleforma-appointments', period_id=period_id)

    app.delete()
    messages.add_message(request, messages.INFO, 'Votre réservation a été annulé.')
    return redirect('teleforma-appointments', period_id=period_id)

