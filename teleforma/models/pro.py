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

from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from teleforma.models.core import *

STATUS_CHOICES = (
		(1, _('Draft')),
		(2, _('Public')),
		(3, _('Close')),
	)


class Seminar(Model):

    course          = ForeignKey(Course, related_name='seminar', verbose_name=_('course'))
    title           = CharField(_('title'), max_length=255, blank=True)
    price           = FloatField(_('price'))
    status			    = IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    rank            = IntegerField(_('rank'))

    doc_1           = ForeignKey(Document, related_name=_("seminar"),
                                        verbose_name=_('doc 1'),
                                        blank=True, null=True)
    media           = ForeignKey(Media, related_name="seminar",
                                        verbose_name=_('media'),
                                        blank=True, null=True)
    doc_2           = ForeignKey(Document, related_name="seminar",
                                        verbose_name=_('doc 2'),
                                        blank=True, null=True)
    doc_correct     = ForeignKey(Document, related_name=_("seminar"),
                                        verbose_name=_('doc_correct'),
                                        blank=True, null=True)

    suscribers      = ManyToManyField(User, related_name="seminar", verbose_name=_('suscribers'),
                                        blank=True, null=True)

    date_added      = DateTimeField(_('date added'), auto_now_add=True)
    date_modified   = DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return '-'.join([self.course, self.rank, self.title])

    class Meta:
        db_table = app_label + '_' + 'seminar'
        verbose_name = _('Seminar')


class Answer(Model):

    user = ForeignKey(User, related_name=_("answer"), verbose_name=_('user'))
    question = ForeignKey(Question, related_name=_("answer"), verbose_name=_('question'))
    answer = TextField(_('answer'))
    status = IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    validated	= BooleanField(_('validated'))

    def __unicode__(self):
        return '-'.join([self.seminar, self.question, self.user])

    class Meta:
        db_table = app_label + '_' + 'answer'
        verbose_name = _('Answer')


class Question(Model):

    seminar = ForeignKey(Seminar, verbose_name=_('seminar'))
    title = CharField(_('title'), max_length=255, blank=True)
    question = TextField(_('question'))
    rank = IntegerField(_('rank'))
    weight = IntegerField(_('weight'))
    min_num_char = IntegerField(_('minimum numbers of characters'))
    status = IntegerField(_('status'), choices=STATUS_CHOICES, default=1)


    def __unicode__(self):
        return '-'.join([self.seminar, self.rank, self.title])

    class Meta:
        db_table = app_label + '_' + 'question'
        verbose_name = _('Question')

class TestimonialTheme(Model):

    organization = ForeignKey(Organization, related_name='testimonial_theme',
                                 verbose_name=_('organization'))
    text = TextField(_('text'))


class Testimonial(Model):

    seminar = ForeignKey(Seminar, verbose_name=_('seminar'))
    user = ForeignKey(User, related_name=_("testimonial"), verbose_name=_('user'))

