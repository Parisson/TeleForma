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
import django.db.models as models
from django.db.models import *
from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tools import *
from telemeta.models.media import *

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

class Department(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    organization    = ForeignKey('Organization', related_name='department', verbose_name='organization')

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'department'



class Category(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'category'



class Course(Model):

    public_id       = CharField(_('public_id'), max_length=255)
    department      = ForeignKey('Department', related_name='course', verbose_name='department')
    title           = CharField(_('title'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    category        = ForeignKey('Category', related_name='student', verbose_name='category')

    class Meta:
        db_table = app_label + '_' + 'course'


class Professor(Model):

    user            = ForeignKey('User', related_name='professor', verbose_name='user')
    courses         = ManyToManyField('Course', related_name="student", verbose_name=_('course'),
                                        blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = app_label + '_' + 'professor'


class Conference(Model):

    title           = CharField(_('title'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)
    professor       = ForeignKey('Professor', related_name='course', verbose_name='professor')
    course          = ForeignKey('Course', related_name='document', verbose_name='course')
    session         = CharField(_('session'), choices=session_choices,
                                      max_length=16, default="1")

    def __str__(self):
        return self.title

    class Meta:
        db_table = app_label + '_' + 'conference'


class IEJ(Model):

    name            = CharField(_('name'), max_length=255)
    description     = CharField(_('description'), max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = app_label + '_' + 'iej'


class Student(Model):

    user            = ForeignKey('User', related_name='student', verbose_name='user')
    category        = ForeignKey('Category', related_name='student', verbose_name='category')
    iej             = ForeignKey('IEJ', related_name='student', verbose_name='iej')
    courses         = ManyToManyField('Course', related_name="student", verbose_name=_('course'),
                                        blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = app_label + '_' + 'student'


class MediaBaseResource(Model):
    "Describe a media base resource"

    title           = CharField(_('title'), required=True)
    description     = CharField(_('description'))
    mime_type       = CharField(_('mime_type'), null=True)
    credits         = CharField(_('credits'))
    is_published    = BooleanField(_('published'))
    date_added      = DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return self.code

    @property
    def public_id(self):
        return self.code

    def get_fields(self):
        return self._meta.fields

    class Meta(MetaCore):
        abstract = True
        ordering = ['code']


class Document(MediaBaseResource):

    element_type = 'document'

    code            = CharField(_('code'))
    course          = ForeignKey('Course', related_name='document', verbose_name='course')
    file            = FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename")

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


class Media(MediaBaseResource):

    element_type = 'media'

    course          = ForeignKey('Course', related_name='media', verbose_name='course')
    item            = ForeignKey('MediaItem', related_name='media', verbose_name='item')

    class Meta:
        db_table = app_label + '_' + 'media'



class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':3, 'cols':30})}
         )
         return super(ShortTextField, self).formfield(**kwargs)

add_introspection_rules([], ["^teleforma\.models\.ShortTextField"])
