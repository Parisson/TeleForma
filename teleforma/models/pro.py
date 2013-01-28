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
from django.conf import settings
import django.db.models as models
from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from teleforma.models.core import *
from forms_builder.forms.models import Form
from django.core.urlresolvers import reverse


class SeminarType(models.Model):

    name            = models.CharField(_('name'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'seminar_type'
        verbose_name = _('Seminar type')


class Seminar(Displayable):

    # title, description, keywords and dates are given by Displayable

    type            = models.ForeignKey(SeminarType, related_name='seminar', verbose_name=_('type'),
                                        blank=True, null=True)
    course          = models.ForeignKey(Course, related_name='seminar', verbose_name=_('course'))
    sub_title       = models.CharField(_('sub title'), max_length=1024, blank=True)
    concerned       = models.CharField(_('public concerned'), max_length=1024, blank=True)
    level           = models.CharField(_('level'), max_length=255, blank=True)
    price           = models.FloatField(_('price'), blank=True, null=True)
    rank            = models.IntegerField(_('rank'), blank=True, null=True)
    magistral       = models.BooleanField(_('magistral'))
    index           = tinymce.models.HTMLField(_('index'), blank=True)
    duration        = DurationField(_('approximative duration'))
    professor       = models.ManyToManyField('Professor', related_name='seminar',
                                            verbose_name=_('professor'), blank=True, null=True)
    docs_description = models.ManyToManyField(Document, related_name="seminar_docs_description",
                                        verbose_name=_('description documents'),
                                        blank=True, null=True)
    docs_1          = models.ManyToManyField(Document, related_name="seminar_docs_1",
                                        verbose_name=_('documents 1'),
                                        blank=True, null=True)
    medias          = models.ManyToManyField(Media, related_name="seminar",
                                        verbose_name=_('media'),
                                        blank=True, null=True)
    media_preview  = models.ForeignKey(Media, related_name="seminar_preview",
                                        verbose_name=_('media_preview'),
                                        blank=True, null=True, on_delete=models.SET_NULL)
    docs_2          = models.ManyToManyField(Document, related_name="seminar_docs_2",
                                        verbose_name=_('documents 2'),
                                        blank=True, null=True)
    docs_correct    = models.ManyToManyField(Document, related_name="seminar_docs_correct",
                                        verbose_name=_('corrected documents'),
                                        blank=True, null=True)
    form            = models.ForeignKey(Form, related_name='seminar', verbose_name=_('form'),
                                        blank=True, null=True)
    date_added      = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return ' - '.join([self.course.title, str(self.rank), self.title])

    def public_url(self):
        """
        Get a public fully qualified URL for the object
        """
        url = reverse('teleforma-seminar-detail', kwargs={'pk':self.id})
        return "%s%s" % (settings.TELEFORMA_MASTER_HOST, url)

    def get_absolute_url(self):
        return reverse('seminar-view', kwargs={"pk": self.id})

    class Meta(MetaCore):
        db_table = app_label + '_' + 'seminar'
        verbose_name = _('Seminar')
        ordering = ['rank']


class Question(models.Model):

    element_type = 'question'

    seminar     = models.ForeignKey(Seminar, related_name="question", verbose_name=_('seminar'))
    title       = models.CharField(_('title'), max_length=255, blank=True)
    description = models.CharField(_('description'), max_length=1024, blank=True)
    question    = tinymce.models.HTMLField(_('question'), blank=True)
    rank        = models.IntegerField(_('rank'), blank=True, null=True)
    weight      = models.IntegerField(_('weight'), choices=WEIGHT_CHOICES, default=1)
    min_nchar   = models.IntegerField(_('minimum numbers of characters'))
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=3)

    def __unicode__(self):
        return ' - '.join([unicode(self.seminar), self.title, str(self.rank)])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'question'
        verbose_name = _('Question')
        ordering = ['rank']


class Answer(models.Model):

    user        = models.ForeignKey(User, related_name="answer", verbose_name=_('user'))
    question    = models.ForeignKey(Question, related_name="answer", verbose_name=_('question'))
    answer      = models.TextField(_('answer'))
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    treated     = models.BooleanField(_('treated'))
    validated   = models.BooleanField(_('validated'))
    date_submitted = models.DateTimeField(_('date submitted'), auto_now=True, null=True)
    date_validated = models.DateTimeField(_('date validated'), null=True)
    date_added     = models.DateTimeField(_('date added'), auto_now_add=True, null=True)

    def __unicode__(self):
        return ' - '.join([unicode(self.question), self.user.username, unicode(self.date_submitted)])

    def validate(self):
        self.validated = True
        self.treated = True
        self.date_validated = datetime.datetime.now()
        self.save()

    def reject(self):
        self.validated = False
        self.treated = True
        self.status = 2
        self.save()

    class Meta(MetaCore):
        db_table = app_label + '_' + 'answer'
        verbose_name = _('Answer')
        ordering = ['-date_submitted', '-date_validated']


class TestimonialTemplate(models.Model):

    organization = models.ForeignKey(Organization, related_name='testimonial_template',
                                 verbose_name=_('organization'))
    description  = models.TextField(_('description'), blank=True)
    comments     = models.TextField(_('comments'), blank=True)
    document     = models.ForeignKey(Document, related_name="testimonial_template",
                                verbose_name=_('template'))

    def __unicode__(self):
        return ' - '.join([self.organization.name, self.description])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'testimonial_template'
        verbose_name = _('Testimonial template')


class Testimonial(models.Model):

    seminar     = models.ForeignKey(Seminar, related_name="testimonial", verbose_name=_('seminar'),
                                    blank=True, null=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(User, related_name="testimonial", verbose_name=_('user'),
                                    blank=True, null=True, on_delete=models.SET_NULL)
    template    = models.ForeignKey(TestimonialTemplate, related_name="testimonial",
                                    verbose_name=_('template'), blank=True, null=True)
    file        = models.FileField(_('file'), upload_to='testimonials/%Y/%m',
                                 blank=True, max_length=1024)
    date_added  = models.DateTimeField(_('date added'), auto_now_add=True, null=True)
    title       = models.CharField(_('title'), max_length=255, blank=True)

    def save(self, **kwargs):
        if self.seminar:
            self.title = ' - '.join([self.seminar.title,
                                    self.user.first_name + ' ' + self.user.last_name,
                                    str(self.date_added)])
        else:
            self.title = ' - '.join([self.user.first_name + ' ' + self.user.last_name, str(self.date_added)])
        super(Testimonial, self).save(**kwargs)

    def __unicode__(self):
        return self.title

    class Meta(MetaCore):
        db_table = app_label + '_' + 'testimonial'
        verbose_name = _('Testimonial')
        ordering = ['date_added']


class Auditor(models.Model):

    user            = models.ForeignKey(User, related_name='auditor', verbose_name=_('user'), unique=True)
    seminars        = models.ManyToManyField('Seminar', related_name="auditor",
                                        verbose_name=_('seminars'),
                                        blank=True, null=True)
    conferences     = models.ManyToManyField(Conference, related_name="auditor",
                                        verbose_name=_('conferences'),
                                        blank=True, null=True)

    platform_only   = models.BooleanField(_('platform only'))
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    gender          = models.CharField(_('gender'), choices=GENDER_CHOICES, max_length=8, blank=True)
    company         = models.CharField(_('Company'), max_length=255, blank=True)
    address         = models.TextField(_('Address'), blank=True)
    postal_code     = models.CharField(_('Postal code'), max_length=255, blank=True)
    city            = models.CharField(_('City'), max_length=255, blank=True)
    country         = models.CharField(_('Country'), max_length=255, blank=True)
    language        = models.CharField(_('Language'), max_length=255, blank=True)
    telephone       = models.CharField(_('Telephone'), max_length=255, blank=True)
    fax             = models.CharField(_('Fax'), max_length=255, blank=True)
    expiration_date = models.DateField(_('Expiration_date'), blank=True, null=True)
    init_password   = models.BooleanField(_('Password initialized'))

    def __unicode__(self):
        try:
            return self.user.last_name + ' ' + self.user.first_name
        except:
            return ''

    class Meta(MetaCore):
        db_table = app_label + '_' + 'auditor'
        verbose_name = _('Auditor')
        ordering = ['user__last_name']


class SeminarRevision(models.Model):

    seminar     = models.ForeignKey(Seminar, related_name="revision", verbose_name=_('seminar'))
    user        = models.ForeignKey(User, related_name="revision", verbose_name=_('user'))
    date        = models.DateTimeField(_('date added'), auto_now_add=True, null=True)

    def __unicode__(self):
        pass

    class Meta(MetaCore):
        db_table = app_label + '_' + 'seminar_revisions'
        verbose_name = _('Seminar revision')
        verbose_name_plural = _('Seminar revisions')
