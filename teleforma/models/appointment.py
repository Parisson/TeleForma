# -*- coding: utf-8 -*-

import datetime

from django.db.models import *
from teleforma.models.core import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers
from django.utils.functional import cached_property
from django.core.cache import cache
CACHE_KEY = 'appointment'


APPOINTMENT_MODE = (('presentiel', 'Presentiel'), ('distance', 'A distance'))

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

class AppointmentPeriod(Model):
    periods = models.ManyToManyField(Period, related_name='appointment_periods',
                                     verbose_name=u"Période")
    name = models.CharField(_('name'), max_length=255)

    course = models.ForeignKey("Course", verbose_name=_("Course"), on_delete=models.SET_NULL, default=19, blank=True, null=True)
    # nb_appointments = models.IntegerField("nombre de rendez-vous autorisé sur la période",
    #                                       default=1)

    start = models.DateField("date de début d'inscription")
    end = models.DateField("date de fin d'inscription")

    enable_appointment = models.BooleanField(_('activer la prise de rendez-vous'),
                                             blank=True, default=True)
    book_delay = models.IntegerField("délai minimal (en jours ouvrables) de prise de rendez-vous",
                                     default=2)
    cancel_delay = models.IntegerField("délai minimal (en jours ouvrables) d'annulation de rendez-vous",
                                       default=2)
    appointment_mail_text = models.TextField("message à inclure dans le mail de confirmation de rendez-vous pour le présentiel",
                                             blank=True, null=True)
    appointment_mail_text_distance = models.TextField("message à inclure dans le mail de confirmation de rendez-vous pour les rendez-vous à distance",
                                             blank=True, null=True)
    appointment_slot_size = models.IntegerField("écart entre les créneaux d'inscription (minutes)", default=40)

    # bbb_room = models.URLField("salon bbb", help_text='Lien vers le salon BBB pour les inscriptions à distance (ex: https://bbb.parisson.com/b/yoa-mtc-a2e). La salle doit avoir été au préalable créé par un membre du jury sur https://bbb.parisson.com.', null=True, blank=True, max_length=200)

    def __unicode__(self):
        return self.name

    def get_appointment(self, user):
        q = Appointment.objects.filter(student=user, slot__appointment_period=self)
        if q:
            return q.get()
        return None

    @property
    def is_open(self):
        """
        Check if the period is open today
        """
        return self.start <= datetime.date.today() <= self.end and self.enable_appointment

    @cached_property
    # @timing
    def days(self):
        days = {}
        delay = self.book_delay
        today = datetime.date.today()

        for slot in AppointmentSlot.objects.filter(appointment_period=self).order_by('start'):
            cache_key = '%s_%s_%s-%s' % (CACHE_KEY, self.id, slot.date, slot.mode)
            dayData = cache.get(cache_key)
            dayData = None
            slot_key = str(slot.date) + "-" + slot.mode
            if not dayData:
                slotData = {'instance':slot,
                            'slots':slot.slots,
                            'mode': slot.mode,
                            'get_visible_jurys':slot.get_visible_jurys,
                            'get_nb_of_visible_jurys':slot.get_nb_of_visible_jurys,
                            'has_available_slot':slot.has_available_slot}
                if slot_key not in days:
                    days[slot_key] = {}
                    days[slot_key]['date'] = slot.date
                    days[slot_key]['mode'] = slot.mode
                    days[slot_key]['slots'] = [slotData, ]
                    days[slot_key]['available'] = False
                else:
                    days[slot_key]['slots'].append(slotData)

                # days are available if they are within the good period and if there are remaining slots
                if slotData['has_available_slot'] and self.work_day_between(today, slot.date) >= delay:
                    days[slot_key]['available'] = True
                days[slot_key]['from_cache'] = False
            else:
                days[slot_key] = dayData
                days[slot_key]['from_cache'] = True

        for day in days:
            if not days[day]['from_cache']:
                cache_key = '%s_%s_%s' % (CACHE_KEY, self.id, day)
                cache.set(cache_key, days[day], 1800)

        # print days
        return sorted(days.values(), key=lambda d:d['date'])

    @cached_property
    def modes(self):
        modes = set()
        for day in self.days:
            if day['mode'] not in modes:
                for MODE in APPOINTMENT_MODE:
                    if MODE[0] == day['mode']:
                        modes.add(MODE)
                        break
        return modes

    @staticmethod
    def work_day_between(start, end):
        """
        Get the number of work days (excluding saturday and sunday) between
        start and end
        """

        # If start and end days are in week-end, find the next/previous working day
        ewd = end.weekday()
        if ewd in (5, 6):
            end -= datetime.timedelta(days=ewd - 4)

        swd = start.weekday()
        if swd in (5, 6):
            start += datetime.timedelta(days=7 - swd)

        # Don't output any negative number of days
        if end <= start:
            return 0

        delta = (end - start).days

        # Handle full weeks
        res = delta / 7 * 5
        delta = delta % 7

        # Check how many days left this week
        weekday = start.weekday()
        remaining = 5 - weekday

        if delta < remaining:
            res += delta
        elif delta < remaining + 2:
            res += remaining
        else:
            res += delta - 2

        return res

    class Meta(MetaCore):
        ordering = ('id',)
        db_table = app_label + '_appointment_period'
        verbose_name = "période de prise de rendez-vous"
        verbose_name_plural = "périodes de prise de rendez-vous"


# class AppointmentDay(Model):
#     appointment_period = models.ForeignKey(AppointmentPeriod,
#                                            related_name = "days",
#                                            verbose_name = u"Période de prise de rendez-vous")
#     date = models.DateField('date')
#
#     def __unicode__(self):
#         return self.date and self.date.strftime('%d/%m/%Y') or u''
#
#     class Meta(MetaCore):
#         db_table = app_label + '_appointment_date'
#         verbose_name = "date de prise de rendez-vous"
#         verbose_name_plural = "dates de prise de rendez-vous"
#


class AppointmentSlot(Model):
    # day = models.ForeignKey(AppointmentDay,
    #                         related_name = 'slots',
    #                         verbose_name = 'jour')
    appointment_period = models.ForeignKey(AppointmentPeriod,
                                           related_name="slots",
                                           verbose_name=u"Période de prise de rendez-vous", null=True, blank=False)
    mode = models.CharField('Mode', choices=APPOINTMENT_MODE, default='presentiel', max_length=20)
    
    date = models.DateField('date', null=True, blank=False)

    start = models.TimeField("heure du premier créneau (heure d'arrivée)")
    nb = models.IntegerField('nombre de créneaux')

    def __unicode__(self):
        return unicode(self.date) + ' ' + (self.start and self.start.strftime('%H:%M') or '')

    class Meta(MetaCore):
        ordering = ('id',)
        db_table = app_label + '_appointment_slot'
        verbose_name = "créneau de rendez-vous"
        verbose_name_plural = "créneaux de rendez-vous"


    # @property
    # def slots_from_same_day(self):
    #     slots = AppointmentSlot.objets.filter(appointment_period=self.appointment_period, date=self.date)

    def get_nb_jury(self):
        return self.jurys.count()
    get_nb_jury.short_description = "Nombre de jurys"

    @property
    def get_visible_jurys(self):
        return self.jurys.order_by('id')[:self.nb_jurys_to_show]

    @property
    def get_nb_of_visible_jurys(self):
        return self.nb_jurys_to_show

    @cached_property
    def nb_jurys_to_show(self):
        min = 100

        for groupslot in AppointmentSlot.objects.filter(date=self.date).all():
            for slot in groupslot.slots:
                for i, jury in enumerate(slot['jurys']):
                    if jury['available']:
                        if i < min:
                            min = i
        return 1 + min

    @cached_property
    def slots(self):
        res = []
        size = self.appointment_period.appointment_slot_size

        # slots reserved per jury
        jurys = self.jurys.all()
        jurys_slots = []

        for jury in jurys:
            jurys_slots.append([ap.slot_nb for ap in self.appointments.filter(jury=jury, slot=self)])

        for i in range(self.nb):
            arrival = datetime.datetime.combine(self.date, self.start) + datetime.timedelta(minutes=i * size)
            if self.mode == 'distance':
                start = arrival
                end = start + datetime.timedelta(minutes=size)
            else:
                start = arrival + datetime.timedelta(minutes=60)
                end = start + datetime.timedelta(minutes=size)
            slot_info = {
                'slot_nb': i,
                'start': start,
                'end': end,
                'arrival': arrival,
            }

            # compute if a slot is available for each jury
            sjurys = []
            for j, jury in enumerate(jurys):
                sjurys.append({'id': jury.id, 'available': i not in jurys_slots[j]})
            slot_info['jurys'] = sjurys
            res.append(slot_info)

            # res.append(self.start + datetime.timedelta(minutes = i * size))
        # print res
        return res

    @cached_property
    def has_available_slot(self):
        """ is this day has any slot available"""
        for slot in self.slots:
            for jury in slot['jurys']:
                if jury['available']:
                    return True
        return False

    @property
    def can_book_today(self):
        delay = self.appointment_period.book_delay
        today = datetime.date.today()
        return self.appointment_period.work_day_between(today, self.date) >= delay


class AppointmentJury(Model):
    slot = models.ForeignKey(AppointmentSlot,
                             related_name='jurys',
                             verbose_name='creneau', null=True, blank=False)

    name = models.CharField(_('name'), max_length=255)
    address = models.TextField("adresse", null=True, blank=True)
    bbb_room = models.URLField("salon bbb", help_text='Lien vers le salon BBB pour les inscriptions à distance (ex: https://bbb.parisson.com/b/yoa-mtc-a2e). La salle doit avoir été au préalable créé par un membre du jury sur https://bbb.parisson.com.', null=True, blank=True, max_length=200)
    # account = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.SET_NULL, blank=True, null=True)


    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        ordering = ('id',)
        db_table = app_label + '_appointment_jury'
        verbose_name = "jury"


class Appointment(Model):
    slot = models.ForeignKey(AppointmentSlot, related_name="appointments",
                             verbose_name=u"créneau")
    student = models.ForeignKey(User, related_name="appointments",
                                verbose_name="étudiant")
    jury = models.ForeignKey(AppointmentJury, related_name="appointments",
                             verbose_name="jury", on_delete=models.SET_NULL, blank=False, null=True)
    slot_nb = models.IntegerField('numéro du créneau')

    def __unicode__(self):
        return u"%s (%s, %s)" % (self.student, self.real_date_human,
                                 self.jury)

    class Meta(MetaCore):
        db_table = app_label + '_appointment'
        verbose_name = "rendez-vous"
        verbose_name_plural = "rendez-vous"
        unique_together = ('slot', 'jury', 'slot_nb')

    @property
    def appointment_period(self):
        return self.slot.appointment_period

    @property
    def day(self):
        return self.slot.date

    @property
    def start(self):
        base = dt = datetime.datetime.combine(datetime.date.today(), self.arrival)
        if self.slot.mode != 'distance':
            dt = base + datetime.timedelta(minutes=60)
        return datetime.time(dt.hour, dt.minute, 0)

    @property
    def end(self):
        dt = datetime.datetime.combine(datetime.date.today(), self.start) + datetime.timedelta(
            minutes=self.appointment_period.appointment_slot_size)
        return datetime.time(dt.hour, dt.minute, 0)

    @property
    def arrival(self):
        """
        arrival hour
        """
        start = self.slot.start
        delta = self.slot_nb * self.appointment_period.appointment_slot_size
        dt = datetime.datetime.combine(datetime.date.today(), start) + datetime.timedelta(minutes=delta)
        return datetime.time(dt.hour, dt.minute, 0)

    @property
    def real_date(self):
        start = self.arrival
        return datetime.datetime.combine(self.day, start)

    @property
    def real_date_human(self):
        return self.real_date.strftime('%d/%m/%Y %H:%M')

    def can_cancel(self):
        delay = self.appointment_period.cancel_delay
        today = datetime.date.today()
        return AppointmentPeriod.work_day_between(today, self.slot.date) >= delay
