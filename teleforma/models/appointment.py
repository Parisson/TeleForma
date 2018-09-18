# -*- coding: utf-8 -*-

import datetime
from datetime import date

from django.db.models import *
from teleforma.models.core import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers
from django.utils.functional import cached_property

class AppointmentPeriod(Model):
    period = models.ForeignKey(Period, related_name='appointment_periods',
                               verbose_name = u"Période")
    name = models.CharField(_('name'), max_length=255)
    nb_appointments = models.IntegerField("nombre de rendez-vous autorisé sur la période",
                                          default=1)

    def __unicode__(self):
        return self.name

    def get_appointment(self, user):
        q = Appointment.objects.filter(student=user, slot__day__appointment_period=self)
        if q:
            return q.get()
        return None

    class Meta(MetaCore):
        db_table = app_label + '_appointment_period'
        verbose_name = "période de prise de rendez-vous"
        verbose_name_plural = "périodes de prise de rendez-vous"

class AppointmentDay(Model):
    appointment_period = models.ForeignKey(AppointmentPeriod,
                                           related_name = "days",
                                           verbose_name = u"Période de prise de rendez-vous")
    date = models.DateField('date')

    def __unicode__(self):
        return self.date and self.date.strftime('%d/%m/%Y') or u''

    class Meta(MetaCore):
        db_table = app_label + '_appointment_date'
        verbose_name = "date de prise de rendez-vous"
        verbose_name_plural = "dates de prise de rendez-vous"

    def changeform_link(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = urlresolvers.reverse(
                'admin:teleforma_appointmentday_change', args=(self.id,)
            )
            return u'<a href="%s" target="_blank">Détails</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header

    def get_nb_slots(self):
        return sum([ s.nb for s in self.slots.all() ])
    get_nb_slots.short_description = 'Nombre de créneaux'

    def get_nb_jury(self):
        return self.jurys.count()
    get_nb_jury.short_description = 'Nombre de jurys'

    @property
    def period(self):
        return self.appointment_period.period

    @cached_property
    def available_jurys(self):
        jurys = self.jurys.order_by('id').all()
        available = []
        for i, jury in enumerate(jurys):
            # first jury is always available
            if i==0:
                available.append(jury)
                continue

            previous_jury_has_slot = False
            has_slot_reserved = False
            for groupslot in self.slots.all():
                for slot in groupslot.slots:
                    if slot['jurys'][i-1]['available']:
                        previous_jury_has_slot = True
                    if not slot['jurys'][i]['available']:
                        has_slot_reserved = True
            # show only jury who have reserved slots or if previous jury has no more slots
            if not previous_jury_has_slot or has_slot_reserved:
                available.append(jury)

        return available

    @property
    def number_of_available_jurys(self):
        return len(self.available_jurys)




class AppointmentSlot(Model):
    day = models.ForeignKey(AppointmentDay,
                            related_name = 'slots',
                            verbose_name = 'jour')

    start = models.TimeField('heure du premier créneau')
    nb = models.IntegerField('nombre de créneaux')

    def __unicode__(self):
        return unicode(self.day) + ' ' + (self.start and self.start.strftime('%H:%M') or '')

    class Meta(MetaCore):
        db_table = app_label + '_appointment_slot'
        verbose_name = "créneau de rendez-vous"
        verbose_name_plural = "créneaux de rendez-vous"

    @property
    def period(self):
        return self.day.period

    # @cached_property
    @property
    def slots(self):
        res = []
        size = self.period.appointment_slot_size

        # slots reserved per jury
        jurys = self.day.jurys.order_by('id').all()
        jurys_slots = []
        for jury in jurys:
            jurys_slots.append([ap.slot_nb for ap in self.appointments.filter(jury=jury)])


        for i in range(self.nb):
            # for jury in self.
            start = datetime.datetime.combine(date.today(), self.start) + datetime.timedelta(minutes = i * size)
            end = start + datetime.timedelta(minutes = size)
            arrival = start - datetime.timedelta(minutes = 60)
            slot_info = {
                'slot_nb':i,
                'start':start,
                'end':end,
                'arrival':arrival,
            }
            sjurys = []
            for j, jury in enumerate(jurys):
                sjurys.append({'id':jury.id, 'available':i not in jurys_slots[j]})
            slot_info['jurys'] = sjurys
            res.append(slot_info)

            # res.append(self.start + datetime.timedelta(minutes = i * size))
        return res

class AppointmentJury(Model):
    day = models.ForeignKey(AppointmentDay,
                            related_name = 'jurys',
                            verbose_name = 'jour')

    name = models.CharField(_('name'), max_length=255)
    address = models.TextField("adresse")

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_appointment_jury'
        verbose_name = "jury"


class Appointment(Model):
    slot = models.ForeignKey(AppointmentSlot, related_name="appointments",
                             verbose_name = u"créneau")
    student = models.ForeignKey(User, related_name = "appointments",
                                verbose_name="étudiant")
    jury = models.ForeignKey(AppointmentJury, related_name="appointments",
                             verbose_name = "jury")
    slot_nb = models.IntegerField('numéro du créneau')

    def __unicode__(self):
        return u"%s (%s, %s)" % (self.student, self.real_date_human,
                                 self.jury)

    class Meta(MetaCore):
        db_table = app_label + '_appointment'
        verbose_name = "rendez-vous"
        verbose_name_plural = "rendez-vous"

    @property
    def period(self):
        return self.slot.period

    @property
    def day(self):
        return self.slot.day

    @property
    def real_time(self):
        start = self.slot.start
        delta = self.slot_nb * self.period.appointment_slot_size
        dt = datetime.datetime.combine(date.today(), start) + datetime.timedelta(minutes = delta)
        return datetime.time(dt.hour,dt.minute,0)

    @property
    def real_date(self):
        return datetime.datetime.combine(self.day.date, self.real_time)

    @property
    def real_date_human(self):
        return self.real_date.strftime('%d/%m/%Y %H:%M')
