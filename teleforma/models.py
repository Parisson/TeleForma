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

from south.modelsinspector import add_introspection_rules

app_label = 'teleforma'

n_sessions = 21
session_choices = [(str(x), str(y)) for x in range(1, n_sessions) for y in range(1, n_sessions) if x == y]


class Organization(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'organization'
        verbose_name = _('organization')

class Department(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    organization    = ForeignKey('Organization', related_name='department', verbose_name=_('organization'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'department'
        verbose_name = _('department')


class Category(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Course(Model):

    department      = ForeignKey('Department', related_name='course', verbose_name=_('department'))
    title           = CharField(_('title'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    category        = ForeignKey('Category', related_name='course', verbose_name=_('category'))
    public_id       = CharField(_('public_id'), max_length=255, blank=True)

    def __str__(self):
        return self.department.name + ' - '  + self.category.name + ' - ' + self.title

    class Meta:
        db_table = app_label + '_' + 'course'
        verbose_name = _('course')


class Professor(Model):

    user            = ForeignKey(User, related_name='professor', verbose_name=_('user'), unique=True)
    courses         = ManyToManyField('Course', related_name="professor", verbose_name=_('courses'),
                                        blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = app_label + '_' + 'professor'
        verbose_name = _('professor')


class Room(Model):

    organization    = ForeignKey('Organization', related_name='room', verbose_name=_('organization'))
    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __str__(self):
        return self.organization.name + ' - ' + self.name

    class Meta:
        db_table = app_label + '_' + 'room'
        verbose_name = _('room')


class Conference(Model):

    title           = CharField(_('title'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    professor       = ForeignKey('Professor', related_name='conference', verbose_name=_('professor'))
    course          = ForeignKey('Course', related_name='conference', verbose_name=_('course'))
    session         = CharField(_('session'), choices=session_choices,
                                      max_length=16, default="1")
    room            = ForeignKey('Room', related_name='conference', verbose_name=_('room'),
                                 null=True, blank=True)
    date_begin      = DateTimeField(_('begin date'), null=True, blank=True)
    date_end        = DateTimeField(_('end date'), null=True, blank=True)

    def __str__(self):
        return self.course.department.name + ' - ' + self.course.title + ' - ' + \
                self.title + ' - ' + self.professor.user.first_name +  ' - ' + \
                self.professor.user.last_name +  ' - ' + str(self.date_begin)

    class Meta:
        db_table = app_label + '_' + 'conference'
        verbose_name = _('conference')


class IEJ(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'iej'
        verbose_name = _('IEJ')
        verbose_name_plural = _('IEJ')


class Student(Model):

    user            = ForeignKey(User, related_name='student', verbose_name=_('user'), unique=True )
    category        = ForeignKey('Category', related_name='student', verbose_name=_('category'))
    iej             = ForeignKey('IEJ', related_name='student', verbose_name=_('iej'))
    courses         = ManyToManyField('Course', related_name="student", verbose_name=_('courses'),
                                        blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = app_label + '_' + 'student'
        verbose_name = _('student')


class MediaBase(Model):
    "Base media resource"

    title           = CharField(_('title'), max_length=255, blank=True)
    description     = CharField(_('description'), max_length=255, blank=True)
    credits         = CharField(_('credits'), max_length=255, blank=True)
    is_published    = BooleanField(_('published'))
    date_added      = DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.item.title

    @property
    def public_id(self):
        return self.code

    def get_fields(self):
        return self._meta.fields

    class Meta:
        abstract = True
        ordering = ['date_added']


class Document(MediaBase):

    element_type = 'document'

    code            = CharField(_('code'), max_length=255, blank=True)
    course          = ForeignKey('Course', related_name='document', verbose_name='course')
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
        if self.title and not re.match('^ *N *$', self.title):
            return  self.title
        else:
            return  unicode(self.title)

    class Meta:
        db_table = app_label + '_' + 'document'


class Media(MediaBase):
    "Describe a media resource linked to a conference and a telemeta item"

    element_type = 'media'

    conference      = ForeignKey('Conference', related_name='media', verbose_name=_('conference'))
    item            = ForeignKey(telemeta.models.media.MediaItem, related_name='media',
                                 verbose_name='item', blank=True, null=True)
    is_live         = BooleanField(_('is live'))

    class Meta:
        db_table = app_label + '_' + 'media'



class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':3, 'cols':30})}
         )
         return super(ShortTextField, self).formfield(**kwargs)

add_introspection_rules([], ["^teleforma\.models\.ShortTextField"])
