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
import tinymce.models


class MediaPackage(MediaBase):
    "Media resource package handling multiple (audio and video) media types"

    element_type    = 'media_package'

    readers         = models.ManyToManyField(User, related_name="media_package", 
                                        verbose_name=_('readers'),
                                        blank=True, null=True)
    audio_items     = models.ManyToManyField(MediaItem, related_name="media_package_audio",
                                        verbose_name=_('audio items'),
                                        blank=True, null=True)
    video_items     = models.ManyToManyField(MediaItem, related_name="media_package_video", 
                                        verbose_name=_('video items'),
                                        blank=True, null=True)
    rank            = models.IntegerField(_('rank'), blank=True, null=True)
    
    def __str__(self):
        if self.title:
            return self.title.encode('utf8')
        elif self.audio_items:
            return self.audio_items.all()[0].title.encode('utf8')
        elif self.video_items:
            return self.video_items.all()[0].title.encode('utf8')

    class Meta(MetaCore):
        db_table = app_label + '_' + 'media_package'


class SeminarType(models.Model):

    name            = models.CharField(_('name'), max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'seminar_type'
        verbose_name = _('Seminar type')


class Seminar(models.Model):

    type            = models.ForeignKey(SeminarType, related_name='seminar', verbose_name=_('type'),
                                        blank=True, null=True)
    course          = models.ForeignKey(Course, related_name='seminar', verbose_name=_('course'))
    title           = models.CharField(_('title'), max_length=255, blank=True)
    sub_title       = models.CharField(_('sub title'), max_length=1024, blank=True)
    description     = models.TextField(_('description'), blank=True)
    concerned       = models.CharField(_('public concerned'), max_length=1024, blank=True)
    level           = models.CharField(_('level'), max_length=255, blank=True)
    price           = models.FloatField(_('price'), blank=True, null=True)
    rank            = models.IntegerField(_('rank'), blank=True, null=True)
    magistral       = models.BooleanField(_('magistral'))
    index           = tinymce.models.HTMLField(_('index'), blank=True)

    keywords        = models.CharField(_('keywords'), max_length=1024, blank=True)
    duration        = DurationField(_('approximative duration'))
    date_begin      = models.DateField(_('begin date'), blank=True, null=True)
    date_end        = models.DateField(_('end date'), blank=True, null=True)
    professor       = models.ManyToManyField('Professor', related_name='seminar', 
                                            verbose_name=_('professor'), blank=True, null=True)

    doc_1           = models.ManyToManyField(DocumentSimple, related_name="seminar_doc1", 
                                        verbose_name=_('document 1'),
                                        blank=True, null=True)
    media           = models.ManyToManyField(MediaPackage, related_name="seminar_media",
                                        verbose_name=_('media'),
                                        blank=True, null=True)
    media_preview   = models.ManyToManyField(MediaPackage, related_name="seminar_media_preview",
                                        verbose_name=_('media_preview'),
                                        blank=True, null=True)
    doc_2           = models.ManyToManyField(DocumentSimple, related_name="seminar_doc2",
                                        verbose_name=_('document 2'),
                                        blank=True, null=True)
    doc_correct     = models.ManyToManyField(DocumentSimple, related_name="seminar_doccorrect",
                                        verbose_name=_('corrected document'),
                                        blank=True, null=True)

    date_added      = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = models.DateTimeField(_('date modified'), auto_now=True)
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2, blank=True)

    def __unicode__(self):
        return ' - '.join([self.course.title, str(self.rank), self.title])

    @property
    def scenario(self):
        self.steps = []
        self.steps.append(self.doc_1)
        self.steps.append(self.media)
        self.steps.append(self.doc_2)
        self.steps.append(self.question)
        self.steps.append(self.doc_correct)
        self.steps.append(self.testimonial)
        return self.steps
    
    def step_append(title, type, objects):
        self.steps.append({'title': title, 'type': type, 'objects': objects })


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
    rank        = models.IntegerField(_('rank'), blank=True)
    weight      = models.IntegerField(_('weight'), choices=WEIGHT_CHOICES, default=1)
    min_nchar   = models.IntegerField(_('minimum numbers of characters'))
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)

    def __unicode__(self):
        return ' - '.join([self.seminar.__unicode__(), str(self.rank), self.title])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'question'
        verbose_name = _('Question')
        ordering = ['rank']


class Answer(models.Model):

    user        = models.ForeignKey(User, related_name="answer", verbose_name=_('user'))
    question    = models.ForeignKey(Question, related_name="answer", verbose_name=_('question'))
    answer      = models.TextField(_('answer'))
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    validated   = models.BooleanField(_('validated'))
    date_submitted = models.DateTimeField(_('date submitted'), auto_now=True, null=True)

    def __unicode__(self):
        return ' - '.join([self.question, self.user])

    def validate(self):
        if len(self.answer) >= self.question.min_nchar:
            self.validated = True
            self.save()

    class Meta(MetaCore):
        db_table = app_label + '_' + 'answer'
        verbose_name = _('Answer')


class TestimonialTemplate(models.Model):

    organization = models.ForeignKey(Organization, related_name='testimonial_template',
                                 verbose_name=_('organization'))
    description  = models.TextField(_('description'), blank=True)
    comments     = models.TextField(_('comments'), blank=True)
    document     = models.ForeignKey(DocumentSimple, related_name="testimonial_template",
                                verbose_name=_('template'))

    def __unicode__(self):
        return ' - '.join([self.organization.name, self.description])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'testimonial_template'
        verbose_name = _('Testimonial template')


class Testimonial(models.Model):

    seminar     = models.ForeignKey(Seminar, related_name="testimonial", verbose_name=_('seminar'))
    user        = models.ForeignKey(User, related_name="testimonial", verbose_name=_('user'))
    template    = models.ForeignKey(TestimonialTemplate, related_name="testimonial", 
                                    verbose_name=_('template'))
    document    = models.ForeignKey(DocumentSimple, related_name="testimonial", 
                                        blank=True, null=True)
    rank            = models.IntegerField(_('rank'), blank=True, null=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'testimonial'
        verbose_name = _('Testimonial')


class Evaluation(models.Model):

    seminar     = models.ForeignKey(Seminar, related_name="evaluation", verbose_name=_('seminar'))
    user        = models.ForeignKey(User, related_name="evaluation", verbose_name=_('user'))
    #TODO

    class Meta(MetaCore):
        db_table = app_label + '_' + 'evaluation'
        verbose_name = _('Evaluation')



class Auditor(models.Model):

    user            = models.ForeignKey(User, related_name='auditor', verbose_name=_('user'), unique=True)
    seminars        = models.ManyToManyField('Seminar', related_name="auditor",
                                        verbose_name=_('seminars'),
                                        blank=True, null=True)

    platform_only   = models.BooleanField(_('platform only'))
    address         = models.TextField(_('Address'), blank=True)
    postal_code     = models.CharField(_('Postal code'), max_length=255, blank=True)
    city            = models.CharField(_('City'), max_length=255, blank=True)
    country         = models.CharField(_('Country'), max_length=255, blank=True)
    language        = models.CharField(_('Language'), max_length=255, blank=True)
    telephone       = models.CharField(_('Telephone'), max_length=255, blank=True)
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

    seminar     = models.ForeignKey(Seminar, related_name="seminar_revision", verbose_name=_('seminar'))
    user        = models.ForeignKey(User, related_name="seminar_revision", verbose_name=_('user'))
    date        = models.DateTimeField(_('date modified'), auto_now=True)
    progress    = models.IntegerField(_('progress'), blank=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'seminar_revisions'
        verbose_name = _('Revision')
        verbose_name_plural = _('Revisions')

    def __unicode__(self):
        return ' '.join([seminar.title, user.last_name, str(date)])


    