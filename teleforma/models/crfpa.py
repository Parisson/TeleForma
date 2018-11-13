#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   teleforma

   Copyright (c) 2012-2017 Guillaume Pellerin <yomguy@parisson.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>
"""

import django.db.models as models
from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from teleforma.models.core import *
from tinymce.models import HTMLField
from  django.db.models import signals

class IEJ(Model):

    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'iej'
        verbose_name = _('IEJ')
        verbose_name_plural = _('IEJ')
        ordering = ['name']


class WebClassGroup(models.Model):

    name = models.CharField(_('name'), max_length=255)
    iejs = models.ManyToManyField('IEJ', related_name="web_class_group", verbose_name=_('IEJ'),
                                        blank=True, null=True)

    class Meta(MetaCore):
        verbose_name = _('web class group')
        verbose_name_plural = _('web class group')
        ordering = ['name']

    def to_json_dict(self):
        data = {'name': self.name,
                'iejs': [iej.name for iej in self.iejs.all()],
                 }
        return data


class Training(Model):

    code = models.CharField(_('code'), max_length=255)
    name = models.CharField(_('name'), max_length=255, blank=True)
    description = models.CharField(_('description'), max_length=512, blank=True)
    period = models.ForeignKey('Period', related_name='training', verbose_name=_('period'), blank=True, null=True)
    parent = models.ForeignKey('Training', related_name='children', verbose_name=_('parent'), blank=True, null=True)
    synthesis_note  = models.ManyToManyField('CourseType', related_name="training_synthesis_note", verbose_name=_('synthesis note'),
                                        blank=True, null=True)
    obligation = models.ManyToManyField('CourseType', related_name="training_obligation",
                                        verbose_name=_('obligations'),
                                        blank=True, null=True)
    procedure = models.ManyToManyField('CourseType', related_name="training_procedure",
                                        verbose_name=_('procedure'),
                                        blank=True, null=True)
    written_speciality = models.ManyToManyField('CourseType', related_name="training_written_speciality",
                                        verbose_name=_('written speciality'),
                                        blank=True, null=True)
    oral_speciality = models.ManyToManyField('CourseType', related_name="training_oral_speciality",
                                        verbose_name=_('oral speciality'),
                                        blank=True, null=True)
    oral_1 = models.ManyToManyField('CourseType', related_name="training_oral_1",
                                        verbose_name=_('oral 1'),
                                        blank=True, null=True)
    oral_2 = models.ManyToManyField('CourseType', related_name="training_oral_2",
                                        verbose_name=_('oral 2'),
                                        blank=True, null=True)
    options = models.ManyToManyField('CourseType', related_name="training_options",
                                        verbose_name=_('options'),
                                        blank=True, null=True)
    magistral = models.ManyToManyField('CourseType', related_name="training_magistral",
                                        verbose_name=_('magistral'),
                                        blank=True, null=True)
    cost = models.FloatField(_('cost'), blank=True, null=True)
    available = models.BooleanField(_('available'))

    def __unicode__(self):
        if self.name and self.period:
            return ' - '.join([self.name, self.period.name])
        else:
            return self.get_code()

    def get_code(self):
        code = self.code
        if self.period:
            code += ' - ' + self.period.name
        return code

    class Meta(MetaCore):
        db_table = app_label + '_' + 'training'
        verbose_name = _('training')


class Student(Model):
    "A student profile"

    user = models.ForeignKey(User, related_name='student', verbose_name=_('user'), unique=True)
    iej = models.ForeignKey('IEJ', related_name='student', verbose_name=_('iej'),
                                 blank=True, null=True, on_delete=models.SET_NULL)
    trainings = models.ManyToManyField('Training', related_name='student_trainings', verbose_name=_('trainings'),
                                      blank=True, null=True)
    training = models.ForeignKey('Training', related_name='student_training', verbose_name=_('training'),
                                      blank=True, null=True, limit_choices_to={'available': True})
    procedure = models.ForeignKey('Course', related_name="procedure_students",
                                        verbose_name=_('procedure'), help_text="Matière de procédure",
                                        blank=True, null=True, limit_choices_to={'procedure': True})
    written_speciality = models.ForeignKey('Course', related_name="written_speciality_students",
                                        verbose_name=_('written speciality'), help_text="Matière juridique de spécialité",
                                        blank=True, null=True, limit_choices_to={'written_speciality': True})
    written_speciality = models.ForeignKey('Course', related_name="written_speciality_2students",
                                    verbose_name=_('written speciality'), help_text="Matière juridique de spécialité",
                                    blank=True, null=True, limit_choices_to={'written_speciality': True})
    oral_speciality = models.ForeignKey('Course', related_name="oral_speciality_students",
                                        verbose_name=_('oral speciality'),
                                        help_text="Matière d’oral de spécialité (matière incluse dans la formation approfondie, en option pour toutes les autres formations)",
                                        blank=True, null=True, limit_choices_to={'oral_speciality': True})
    oral_1 = models.ForeignKey('Course', related_name="oral_1_students", verbose_name=_('oral de langue (option)'),
                                        help_text="Matière d’oral de langue (en option)",
                                        blank=True, null=True, limit_choices_to={'oral_1': True})
    oral_2 = models.ForeignKey('Course', related_name="oral_2_students", verbose_name=_('oral 2 (option)'),
                                        help_text="Matière d’oral technique 2 (en option)",
                                        blank=True, null=True, limit_choices_to={'oral_2': True})
    options = models.ForeignKey('Course', related_name="options_students", verbose_name=_('options'),
                                        blank=True, null=True)
    period = models.ForeignKey('Period', related_name='student', verbose_name=_('period'),
                                 blank=True, null=True, on_delete=models.SET_NULL)
    platform_only   = models.BooleanField(_('e-learning platform only'))
    application_fees = models.BooleanField(_('application fees'), blank=True)
    default_application_fees = 40
    subscription_fees = models.FloatField(_('subscription fees'), help_text='€', blank=True, null=True)
    promo_code = models.CharField(_('promo code'), blank=True, max_length=100)
    date_registered = models.DateTimeField(_('registration date'), auto_now_add=True, null=True, blank=True)
    date_subscribed = models.DateTimeField(_('subscription date'), null=True, blank=True)
    is_subscribed = models.BooleanField(_('subscribed'))
    confirmation_sent = models.BooleanField(_('confirmation sent'))
    level = models.CharField(_('studying level'), blank=True, max_length=100)

    balance = models.FloatField(_('balance de paiement'), help_text='€', blank=True, null=True)
    
    def __unicode__(self):
        try:
            return self.user.last_name + ' ' + self.user.first_name
        except:
            return ''

    @property
    def total_fees(self):
        amount = 0
        if self.subscription_fees:
            amount += self.subscription_fees
        if self.application_fees:
            amount += self.default_application_fees
        for optional_fee in self.optional_fees.all():
            amount += optional_fee.value
        for discount in self.discounts.all():
            amount -= discount.value
        return amount

    @property
    def total_payments(self):
        amount = 0
        for payment in self.payments.all():
            amount += payment.value
        return amount

    @property
    def total_discount(self):
        amount = 0
        for discount in self.discounts.all():
            amount -= discount.value
        return amount

    @property
    def total_paybacks(self):
        amount = 0
        for payback in self.paybacks.all():
            amount -= payback.value
        return amount
        
    def update_balance(self):
        old = self.balance
        new = round(self.total_payments - self.total_fees, 2)
        if old != new:
            self.balance = new
            self.save()

    def get_absolute_url(self):
        return reverse_lazy('teleforma-profile-detail', kwargs={'username':self.user.username})

    class Meta(MetaCore):
        db_table = app_label + '_' + 'student'
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['user__last_name', '-date_subscribed']

def update_balance_signal(sender, instance, *args, **kwargs):
    if sender is Student:
        instance.update_balance()
    elif sender in (Discount, OptionalFee, Payment):
        instance.student.update_balance()
        
signals.post_save.connect(update_balance_signal)
signals.post_delete.connect(update_balance_signal)

class Profile(models.Model):
    "User profile extension"

    user = models.ForeignKey(User, related_name='profile', verbose_name=_('user'), unique=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    address_detail = models.CharField(_('Address detail'), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_('Postal code'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=255, blank=True)
    country = models.CharField(_('Country'), max_length=255, blank=True)
    language = models.CharField(_('Language'), max_length=255, blank=True)
    telephone = models.CharField(_('Telephone'), max_length=255, blank=True)
    expiration_date = models.DateField(_('Expiration_date'), blank=True, null=True)
    init_password = models.BooleanField(_('Password initialized'))
    wifi_login = models.CharField(_('WiFi login'), max_length=255, blank=True)
    wifi_pass = models.CharField(_('WiFi pass'), max_length=255, blank=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True, help_text="jj/mm/aaaa")

    class Meta(MetaCore):
        db_table = app_label + '_' + 'profiles'
        verbose_name = _('profile')


months_choices = []
for i in range(1,13):
    months_choices.append((i, datetime.date(2015, i, 1).strftime('%B')))


class Payment(models.Model):
    "a payment from a student"

    student = models.ForeignKey(Student, related_name='payments', verbose_name=_('student'))
    value = models.FloatField(_('amount'), help_text='€')
    month = models.IntegerField(_('month'), choices=months_choices, default=1)
    collected = models.BooleanField(_('collected'))
    type = models.CharField(_('payment type'), choices=payment_choices, max_length=64)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'payments'
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ['month']


class Discount(models.Model):
    "a discount for a student subscription"

    student = models.ForeignKey(Student, related_name='discounts', verbose_name=_('student'))
    value = models.FloatField(_('amount'), help_text='€')
    description = models.CharField(_('description'), max_length=255, blank=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'discounts'
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class OptionalFee(models.Model):
    "an optional fee for a student subscription"

    student = models.ForeignKey(Student, related_name='optional_fees', verbose_name=_('student'))
    value = models.FloatField(_('amount'), help_text='€')
    description = models.CharField(_('description'), max_length=255, blank=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'optional_fees'
        verbose_name = _("Optional fees")
        verbose_name_plural = _("Optional fees")


class Payback(models.Model):
    "an payback for a student subscription"

    student = models.ForeignKey(Student, related_name='paybacks', verbose_name=_('student'))
    value = models.FloatField(_('amount'), help_text='€')
    description = models.CharField(_('description'), max_length=255, blank=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'paybacks'
        verbose_name = _("Payback")
        verbose_name_plural = _("Paybacks")


class Home(models.Model):

    text = HTMLField('Texte', blank=True)
    video = models.ForeignKey(Media, verbose_name="Video", null=True, blank=True)

    class Meta(MetaCore):
        verbose_name = "Page d'accueil"
        verbose_name_plural = "Page d'accueil"

    def __unicode__(self):
        return "Page d'accueil"

    def save(self, *args, **kwargs):
        if Home.objects.exists() and not self.pk:
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('There is can be only one Home instance')
        return super(Home, self).save(*args, **kwargs)


class NewsItem(models.Model):

    title = models.CharField(_('Title'), max_length=255)
    course = models.ForeignKey(Course, related_name='newsitems', verbose_name=_('course'))
    period = models.ForeignKey('Period', related_name='newsitems', verbose_name=_('period'), blank=False, null=True)
    text = HTMLField('Texte')

    created = models.DateTimeField(_('date created'), auto_now_add=True)
    creator = models.ForeignKey(User, related_name='newsitems', verbose_name="Créateur")
    deleted = models.BooleanField('Supprimé')

    class Meta(MetaCore):
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __unicode__(self):
        return "NewsItem %s" % str(self.id)


    def can_edit(self, request):
        return request.user.is_staff or request.user.id == self.creator.id

    def can_delete(self, request):
        return request.user.is_staff or request.user.id == self.creator.id



