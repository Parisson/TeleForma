#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   teleforma

   Copyright (c) 2006-2012 Guillaume Pellerin <yomguy@parisson.com>

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


# CRFPA

class IEJ(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'iej'
        verbose_name = _('IEJ')
        verbose_name_plural = _('IEJ')
        ordering = ['name']


class Training(Model):

    code            = CharField(_('code'), max_length=255)
    name            = CharField(_('name'), max_length=255, blank=True)
    period          = ForeignKey('Period', related_name='training', verbose_name=_('period'),
                                 blank=True, null=True)
    synthesis_note  = ManyToManyField('CourseType', related_name="training_synthesis_note",
                                        verbose_name=_('synthesis note'),
                                        blank=True, null=True)
    obligation      = ManyToManyField('CourseType', related_name="training_obligation",
                                        verbose_name=_('obligations'),
                                        blank=True, null=True)
    procedure       = ManyToManyField('CourseType', related_name="training_procedure",
                                        verbose_name=_('procedure'),
                                        blank=True, null=True)
    written_speciality = ManyToManyField('CourseType', related_name="training_written_speciality",
                                        verbose_name=_('written speciality'),
                                        blank=True, null=True)
    oral_speciality = ManyToManyField('CourseType', related_name="training_oral_speciality",
                                        verbose_name=_('oral speciality'),
                                        blank=True, null=True)
    oral_1          = ManyToManyField('CourseType', related_name="training_oral_1",
                                        verbose_name=_('oral 1'),
                                        blank=True, null=True)
    oral_2          = ManyToManyField('CourseType', related_name="training_oral_2",
                                        verbose_name=_('oral 2'),
                                        blank=True, null=True)
    options         = ManyToManyField('CourseType', related_name="training_options",
                                        verbose_name=_('options'),
                                        blank=True, null=True)
    magistral       = ManyToManyField('CourseType', related_name="training_magistral",
                                        verbose_name=_('magistral'),
                                        blank=True, null=True)
    cost            = FloatField(_('cost'), blank=True, null=True)

    def __unicode__(self):
        code = self.code
        if self.period:
            code += ' - ' + self.period.name
        return code

    class Meta(MetaCore):
        db_table = app_label + '_' + 'training'
        verbose_name = _('training')


class Student(Model):

    user            = ForeignKey(User, related_name='student', verbose_name=_('user'), unique=True)
    #period          = ManyToManyField('Period', related_name='student', verbose_name=_('period'),
    #                             blank=True, null=True)
    iej             = ForeignKey('IEJ', related_name='student', verbose_name=_('iej'),
                                 blank=True, null=True, on_delete=models.SET_NULL)
    #training        = ForeignKey('Training', related_name='student', verbose_name=_('training'),
    #                             blank=True, null=True, on_delete=models.SET_NULL)
    trainings       = ManyToManyField('Training', related_name='student_trainings', verbose_name=_('trainings'),
                                      blank=True, null=True)
    platform_only   = BooleanField(_('platform only'))
    procedure       = ForeignKey('Course', related_name="procedure",
                                        verbose_name=_('procedure'),
                                        blank=True, null=True)
    written_speciality = ForeignKey('Course', related_name="written_speciality",
                                        verbose_name=_('written speciality'),
                                        blank=True, null=True)
    oral_speciality = ForeignKey('Course', related_name="oral_speciality",
                                        verbose_name=_('oral speciality'),
                                        blank=True, null=True)
    oral_1          = ForeignKey('Course', related_name="oral_1", verbose_name=_('oral 1'),
                                        blank=True, null=True)
    oral_2          = ForeignKey('Course', related_name="oral_2", verbose_name=_('oral 2'),
                                        blank=True, null=True)
    options         = ForeignKey('Course', related_name="options", verbose_name=_('options'),
                                        blank=True, null=True)

    def __unicode__(self):
        try:
            return self.user.last_name + ' ' + self.user.first_name
        except:
            return ''

    class Meta(MetaCore):
        db_table = app_label + '_' + 'student'
        verbose_name = _('CRFPA Profile')
        ordering = ['user__last_name']


class Profile(models.Model):
    "User profile extension"

    user            = ForeignKey(User, related_name='profile', verbose_name=_('user'), unique=True)
    address         = TextField(_('Address'), blank=True)
    postal_code     = CharField(_('Postal code'), max_length=255, blank=True)
    city            = CharField(_('City'), max_length=255, blank=True)
    country         = CharField(_('Country'), max_length=255, blank=True)
    language        = CharField(_('Language'), max_length=255, blank=True)
    telephone       = CharField(_('Telephone'), max_length=255, blank=True)
    expiration_date = DateField(_('Expiration_date'), blank=True, null=True)
    init_password   = BooleanField(_('Password initialized'))
    wifi_login      = CharField(_('WiFi login'), max_length=255, blank=True)
    wifi_pass       = CharField(_('WiFi pass'), max_length=255, blank=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'profiles'
        verbose_name = _('profile')


