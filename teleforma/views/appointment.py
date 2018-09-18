# -*- coding: utf-8 -*-

from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404, render

from teleforma.models.appointment import AppointmentPeriod, Appointment, AppointmentDay, AppointmentSlot

from teleforma.views.core import get_periods

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError

class Appointments(View):
    template_name = 'teleforma/appointments.html'

    def check_rights(self, user, period_id):
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse('teleforma-login'))
        student = user.student.all().count()
        if not student:
            return HttpResponse('Unauthorized', status=401)
        periods = [ int(p.id) for p in get_periods(user) ]
        if not int(period_id) in periods:
            return HttpResponse('Unauthorized', status=401)
        return

    def render(self, request, period_id, msg = None):
        # Ensure user is logged in, a student, and has access to current period
        user = request.user

        # Get info
        ap_periods = []
        for ap_period in AppointmentPeriod.objects.filter(period=period_id).order_by('id'):
            ap_periods.append({
                'days':ap_period.days.all(),
                'appointments':ap_period.get_appointment(user)
            })
        # for ap_period in ap_periods:
        #     appointments[ap_period.id] = ap_period.get_appointments(request.user)
        return render(request, self.template_name, {'ap_periods': ap_periods,
                                                    'msg': msg})

    def check_validity(self, user, slot_id, slot_nb, jury_id, day_id):
        """
        Check if we can register to this exact slot
        """
        day = get_object_or_404(AppointmentDay, id = day_id)

        # Check the period is open
        if not day.appointment_period.is_open:
            return u"La période d'inscription n'est pas ouverte"
        # Check we are least delay (ie, 48h) before the date
        if not day.can_book_today():
            delay = day.book_delay
            return u"Vous devez réserver au moins %d jours ouvrés à l'avance" % delay
        # Check if this jury is open
        jurys = day.available_jurys
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
        if day.appointment_period.get_appointment(user):
            return u"Vous avez déjà un rendez-vous"

    def post(self, request, period_id):

        user = request.user
        rights = self.check_rights(user, period_id)
        if rights:
            return rights

        slot_nb = int(request.POST.get('slot_nb'))
        slot_id = int(request.POST.get('slot'))
        jury_id = int(request.POST.get('jury'))
        day_id = int(request.POST.get('day'))

        msg = self.check_validity(user, slot_id, slot_nb, jury_id, day_id)

        if not msg:
            ap = Appointment()
            ap.slot_nb = slot_nb
            ap.slot_id = slot_id
            ap.jury_id = jury_id
            ap.day_id = day_id
            ap.student = user
            try:
                ap.save()
            except IntegrityError:
                # Duplicate appointment caught by the db
                msg = u"Ce créneau n'est plus disponible"
        return self.render(request, period_id, msg = msg)

    def get(self, request, period_id):
        rights = self.check_rights(request.user, period_id)
        if rights:
            return rights
        return self.render(request, period_id)

