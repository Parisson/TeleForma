from django.views.generic import View
from django.shortcuts import render

from teleforma.models.appointment import AppointmentPeriod, Appointment


class Appointments(View):
    template_name = 'teleforma/appointments.html'

    def render(self, request, period_id):
        ap_periods = []
        for ap_period in AppointmentPeriod.objects.filter(period=period_id).order_by('id'):
            ap_periods.append({
                'days':ap_period.days.all(),
                'appointments':ap_period.get_appointment(request.user)
            })
        # for ap_period in ap_periods:
        #     appointments[ap_period.id] = ap_period.get_appointments(request.user)
        return render(request, self.template_name, {'ap_periods': ap_periods})

    def post(self, request, period_id):


        slot_nb = int(request.POST.get('slot_nb'))
        slot_id = int(request.POST.get('slot'))
        jury_id = int(request.POST.get('jury'))
        day_id = int(request.POST.get('day'))

        # TODO : verifier que l'appointment est libre, sinon rediriger vers une page d'erreur
        ap = Appointment()
        ap.slot_nb = slot_nb
        ap.slot_id = slot_id
        ap.jury_id = jury_id
        ap.day_id = day_id
        ap.student = request.user
        ap.save()
        return self.render(request, period_id)

    def get(self, request, period_id):
        return self.render(request, period_id)

