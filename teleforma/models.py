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

import os
import re
import pwd
import time
import urllib
import datetime
import mimetypes
import telemeta
import django.db.models as models
from django.db.models import *
from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from teleforma.fields import *
from django.contrib.contenttypes import generic
from notes.models import Note
import jqchat.models

app_label = 'teleforma'

n_sessions = 21
session_choices = [(str(x), str(y)) for x in range(1, n_sessions) for y in range(1, n_sessions) if x == y]


class Organization(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'organization'
        verbose_name = _('organization')

class Department(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    organization    = ForeignKey('Organization', related_name='department', verbose_name=_('organization'))

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'department'
        verbose_name = _('department')


class Category(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

class CourseType(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'course_type'
        verbose_name = _('type')

class Course(Model):

    department      = ForeignKey('Department', related_name='course', verbose_name=_('department'))
    title           = CharField(_('title'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    type            = ForeignKey('CourseType', related_name='course', verbose_name=_('course type'))
    code            = CharField(_('code'), max_length=255)
    chat_room       = OneToOneField(jqchat.models.Room, help_text='Chat room to be used for this lobby.',
                                    blank=True, null=True)

    notes = generic.GenericRelation(Note)

    def __unicode__(self):
        return ' - '.join([self.department.name, self.title, self.type.name])

    class Meta:
        db_table = app_label + '_' + 'course'
        verbose_name = _('course')


class Professor(Model):

    user            = ForeignKey(User, related_name='professor', verbose_name=_('user'), unique=True)
    courses         = ManyToManyField('Course', related_name="professor", verbose_name=_('courses'),
                                        blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = app_label + '_' + 'professor'
        verbose_name = _('professor')


class Room(Model):

    organization    = ForeignKey('Organization', related_name='room', verbose_name=_('organization'))
    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.organization.name + ' - ' + self.name

    class Meta:
        db_table = app_label + '_' + 'room'
        verbose_name = _('room')


class Conference(Model):

    course          = ForeignKey('Course', related_name='conference', verbose_name=_('course'))
    professor       = ForeignKey('Professor', related_name='conference', verbose_name=_('professor'))
    session         = CharField(_('session'), choices=session_choices,
                                      max_length=16, default="1")
    room            = ForeignKey('Room', related_name='conference', verbose_name=_('room'),
                                 null=True, blank=True)
    comment         = CharField(_('comment'), max_length=255, blank=True)
    date_begin      = DateTimeField(_('begin date'), null=True, blank=True)
    date_end        = DateTimeField(_('end date'), null=True, blank=True)

    @property
    def description(self):
        return ' - '.join([self.course.department.name, self.course.title, self.course.type.name,
                           self.session, self.professor.user.first_name, self.professor.user.last_name,
                           str(self.date_begin)])

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = app_label + '_' + 'conference'
        verbose_name = _('conference')


class MediaBase(Model):
    "Base media resource"

    credits         = CharField(_('credits'), max_length=255, blank=True)
    is_published    = BooleanField(_('published'))
    date_added      = DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = DateTimeField(_('date modified'), auto_now=True)

    notes = generic.GenericRelation(Note)

    def get_fields(self):
        return self._meta.fields

    class Meta:
        abstract = True
        ordering = ['date_added']


class Document(MediaBase):

    element_type = 'document'

    title           = CharField(_('title'), max_length=255, blank=True)
    description     = CharField(_('description'), max_length=255, blank=True)
    code            = CharField(_('code'), max_length=255, blank=True)
    course          = ForeignKey('Course', related_name='document', verbose_name='course')
    conference      = ForeignKey('Conference', related_name='document', verbose_name=_('conference'),
                                 blank=True, null=True)
    is_annal        = BooleanField(_('annal'))
    file            = FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename", blank=True)

    def is_image(self):
        is_url_image = False
        if self.url:
            url_types = ['.png', '.jpg', '.gif', '.jpeg']
            for type in url_types:
                if type in self.url or type.upper() in self.url:
                    is_url_image = True
        return 'image' in self.mime_type or is_url_image

    def set_mime_type(self):
        if self.file:
            self.mime_type = mimetypes.guess_type(self.file.path)[0]

    def __unicode__(self):
        return  ' - '.join([self.title, unicode(self.course)])

    class Meta:
        db_table = app_label + '_' + 'document'


class Media(MediaBase):
    "Describe a media resource linked to a conference and a telemeta item"

    element_type = 'media'

    course          = ForeignKey('Course', related_name='media', verbose_name='course')
    conference      = ForeignKey('Conference', related_name='media', verbose_name=_('conference'),
                                 blank=True, null=True)
    item            = ForeignKey(telemeta.models.media.MediaItem, related_name='media',
                                 verbose_name='item', blank=True, null=True)
    is_live         = BooleanField(_('is live'))


    def __unicode__(self):
        description = self.course.title
        if self.item:
            return description + ' _ ' + self.item.title
        else:
            return description

    class Meta:
        db_table = app_label + '_' + 'media'


# STUDENT

class IEJ(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'iej'
        verbose_name = _('IEJ')
        verbose_name_plural = _('IEJ')
        ordering = ['name']


class Training(Model):

    code            = CharField(_('code'), max_length=255)
    name            = CharField(_('name'), max_length=255, blank=True)
    category        = ForeignKey('Category', related_name='course', verbose_name=_('category'))
    courses         = ManyToManyField('Course', related_name="training", verbose_name=_('courses'),
                                        blank=True, null=True)
    synthesis_note  = BooleanField(_('synthesis note'))
    obligation      = BooleanField(_('obligation'))

    def __unicode__(self):
        return self.code + ' - ' + self.category.name

    class Meta:
        db_table = app_label + '_' + 'training'
        verbose_name = _('training')


class Procedure(Model):

    name           = CharField(_('name'), max_length=255, blank=True)
    code           = CharField(_('code'), max_length=255)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = app_label + '_' + 'procedure'
        verbose_name = _('procedure')


class Speciality(Model):

    name           = CharField(_('name'), max_length=255, blank=True)
    code           = CharField(_('code'), max_length=255)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = app_label + '_' + 'speciality'
        verbose_name = _('speciality')


class Oral(Model):

    name           = CharField(_('name'), max_length=255, blank=True)
    code           = CharField(_('code'), max_length=255)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = app_label + '_' + 'oral'
        verbose_name = _('oral')


class Student(Model):

    user            = ForeignKey(User, related_name='student', verbose_name=_('user'), unique=True )
    category        = ForeignKey('Category', related_name='student', verbose_name=_('category'))
    iej             = ForeignKey('IEJ', related_name='student', verbose_name=_('iej'))
    training        = ForeignKey('Training', related_name='student',
                                 verbose_name=_('training'), blank=True, null=True)
    procedure       = ForeignKey('Procedure', related_name='student',
                                 verbose_name=_('procedure'), blank=True, null=True)
    oral_speciality = ForeignKey('Speciality', related_name='student_oral_spe',
                                 verbose_name=_('oral speciality'), blank=True, null=True)
    written_speciality = ForeignKey('Speciality', related_name='student_written_spe',
                                verbose_name=_('written speciality'), blank=True, null=True)
    oral_1          = ForeignKey('Oral', related_name='oral_1',
                                 verbose_name=_('oral 1'), blank=True, null=True)
    oral_2          = ForeignKey('Oral', related_name='oral_2',
                                 verbose_name=_('oral 1'), blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = app_label + '_' + 'student'
        verbose_name = _('student')


class Profile(models.Model):
    "User profile extension"

    user            = ForeignKey(User, related_name='profile', verbose_name=_('user'), unique=True)
    address         = TextField(_('Address'))
    postal_code     = CharField(_('Postal code'), max_length=255)
    city            = CharField(_('City'), max_length=255)
    country         = CharField(_('Country'), max_length=255, blank=True)
    language        = CharField(_('Language'), max_length=255, blank=True)
    telephone       = CharField(_('Telephone'), max_length=255, blank=True)
    expiration_date = DateField(_('Expiration_date'), blank=True, null=True)
    init_password   = BooleanField(_('Password initialization'))

    class Meta:
        db_table = app_label + '_' + 'profiles'
        verbose_name = _('profile')

