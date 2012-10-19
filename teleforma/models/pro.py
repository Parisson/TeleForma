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


class Seminar(Model):

    course          = models.ForeignKey(Course, related_name='seminar', verbose_name=_('course'))
    title           = models.CharField(_('title'), max_length=255, blank=True)
    price           = models.FloatField(_('price'), blank=True, null=True)
    status			= models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1, blank=True)
    rank            = models.IntegerField(_('rank'))

    doc_1           = models.ForeignKey(DocumentSimple, related_name="seminar_doc1", 
                                        verbose_name=_('document 1'),
                                        blank=True, null=True)
    media           = models.ForeignKey(Media, related_name="seminar",
                                        verbose_name=_('media'),
                                        blank=True, null=True)
    doc_2           = models.ForeignKey(DocumentSimple, related_name="seminar_doc2",
                                        verbose_name=_('document 2'),
                                        blank=True, null=True)
    doc_correct     = models.ForeignKey(DocumentSimple, related_name="seminar_doccorrect",
                                        verbose_name=_('corrected document'),
                                        blank=True, null=True)

    suscribers      = models.ManyToManyField(User, related_name="seminar", verbose_name=_('suscribers'),
                                        blank=True, null=True)

    date_added      = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = models.DateTimeField(_('date modified'), auto_now=True)
    duration        = DurationField(_('approximative duration'))
    keywords        = models.CharField(_('keywords'), max_length=1024, blank=True)

    def __unicode__(self):
        return ' - '.join([self.course.title, str(self.rank), self.title])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'seminar'
        verbose_name = _('Seminar')


class Question(Model):

    seminar     = models.ForeignKey(Seminar, verbose_name=_('seminar'))
    title       = models.CharField(_('title'), max_length=255, blank=True)
    question    = models.TextField(_('question'))
    rank        = models.IntegerField(_('rank'))
    weight      = models.IntegerField(_('weight'), choices=WEIGHT_CHOICES, default=1)
    min_nchar   = models.IntegerField(_('minimum numbers of characters'))
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)


    def __unicode__(self):
        return ' - '.join([self.seminar.__unicode__(), str(self.rank), self.title])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'question'
        verbose_name = _('Question')


class Answer(Model):

    user        = models.ForeignKey(User, related_name=_("answer"), verbose_name=_('user'))
    question    = models.ForeignKey(Question, related_name=_("answer"), verbose_name=_('question'))
    answer      = models.TextField(_('answer'))
    status      = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    validated   = models.BooleanField(_('validated'))

    def __unicode__(self):
        return ' - '.join([self.question, self.user])

    def validate(self):
        if len(self.answer) >= self.question.min_nchar:
            self.validated = True
            self.save()

    class Meta(MetaCore):
        db_table = app_label + '_' + 'answer'
        verbose_name = _('Answer')


class TestimonialTemplate(Model):

    organization = models.ForeignKey(Organization, related_name='testimonial_template',
                                 verbose_name=_('organization'))
    description  = models.TextField(_('description'), blank=True)
    comments     = models.TextField(_('comments'), blank=True)
    document     = models.ForeignKey(DocumentSimple, related_name=_("testimonial_template"),
                                verbose_name=_('template'))

    def __unicode__(self):
        return ' - '.join([self.organization.name, self.description])

    class Meta(MetaCore):
        db_table = app_label + '_' + 'testimonial_template'
        verbose_name = _('Testimonial template')


class Testimonial(Model):

    seminar     = models.ForeignKey(Seminar, verbose_name=_('seminar'))
    user        = models.ForeignKey(User, related_name=_("testimonial"), verbose_name=_('user'))
    template    = models.ForeignKey(TestimonialTemplate, related_name=_("testimonial"), 
                                    verbose_name=_('testimonial_template'))
    document    = models.ForeignKey(DocumentSimple, related_name=_("testimonial"), 
                                        blank=True, null=True)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'testimonial'
        verbose_name = _('Testimonial')

