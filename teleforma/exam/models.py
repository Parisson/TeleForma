#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   TeleForma

   Copyright (c) 2014 Guillaume Pellerin <yomguy@parisson.com>

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

import os, uuid, time, hashlib, mimetypes, tempfile

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Max, Min
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from teleforma.models import Course

app = 'teleforma'

class MetaCore:

    app_label = 'exam'


SCRIPT_STATUS = ((0, _('rejected')), (1, _('draft')), (2, _('pending')), (3, _('corrected')),)
REJECT_REASON = ((0, _('unreadable')), (1, _('bad orientation')), (2, _('bad framing')), (3, _('incomplete')),)

cache_path = settings.MEDIA_ROOT + 'cache/'
script_path = settings.MEDIA_ROOT + 'scripts/'


def sha1sum_file(filename):
    '''
    Return the secure hash digest with sha1 algorithm for a given file

    >>> wav_file = 'tests/samples/guitar.wav' # doctest: +SKIP
    >>> print sha1sum_file(wav_file)
    08301c3f9a8d60926f31e253825cc74263e52ad1
    '''
    import hashlib
    import io

    sha1 = hashlib.sha1()
    chunk_size = sha1.block_size * io.DEFAULT_BUFFER_SIZE

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha1.update(chunk)
    return sha1.hexdigest()

def mimetype_file(path):
    return mimetypes.guess_type(path)[0]


def set_file_properties(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        if not instance.mime_type:
            instance.mime_type = mimetype_file(instance.file.path)
        if not instance.sha1:
            instance.sha1 = sha1sum_file(instance.file.path)
        try:
            if not instance.image:
                path = cache_path + os.sep + instance.uuid + '.jpg'
                command = 'convert ' + instance.file.path + ' ' + path
                os.system(command)
                instance.image = path
        except:
            pass

def check_unique_mimetype(l):
    i = 0
    for d in l:
        mime_type = d['obj'].mime_type
        if not i:
            unique = True
        else:
            unique = unique and (last_type == mime_type)
        last_type = mime_type
        i += 1
    return unique


class Corrector(models.Model):

    user = models.ForeignKey(User, related_name="correctors", verbose_name=_('user'), blank=True, null=True)

    class Meta(MetaCore):
        verbose_name = _('Corrector')
        verbose_name_plural = _('Correctors')

    def __unicode__(self):
        return ' '.join([self.user.first_name, self.user.last_name, str(self.id)])


class Quota(models.Model):

    course = models.ForeignKey(Course, related_name="quotas", verbose_name=_('course'), blank=True, null=True)
    corrector = models.ForeignKey('Corrector', related_name="quotas", verbose_name=_('corrector'), blank=True, null=True)
    value = models.IntegerField(_('value'))

    class Meta(MetaCore):
        verbose_name = _('Quota')
        verbose_name_plural = _('Quotas')

    def __unicode__(self):
        return ' - '.join([self.course.title, str(self.value)])
    
    @property
    def level(self):
        if self.value:
            if self.value != 0:
                return 100*self.corrector.scripts.filter(Q(status=2) | Q(status=3)).count()/self.value
            else:
                return 0
        else:
            return 0


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True, null=True)
    uuid = models.CharField(_('UUID'), unique=True, blank=True, max_length=512)
    mime_type = models.CharField(_('MIME type'), max_length=128, blank=True)
    sha1 = models.CharField(_('sha1'), blank=True, max_length=512)

    class Meta(MetaCore):
        abstract = True
    
    def save(self, **kwargs):
        super(BaseResource, self).save(**kwargs)
        if not self.uuid:
            self.uuid = unicode(uuid.uuid4())

    def __unicode__(self):
        return self.uuid


class Exam(BaseResource):
    """Examination"""

    course = models.ForeignKey(Course, related_name="exams", verbose_name=_('courses'), blank=True, null=True, on_delete=models.SET_NULL)
    session = models.IntegerField(_('Session'), blank=True, null=True)
    author = models.ForeignKey(User, related_name="exams", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('title'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)    
    credits = models.TextField(_('credits'), blank=True)
    file = models.FileField(_('File'), upload_to='exams/%Y/%m/%d', blank=True)
    note = models.IntegerField(_('Maximum note'), blank=True, null=True)
    
    class Meta(MetaCore):
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')

class ScriptPage(BaseResource):

    script = models.ForeignKey('Script', related_name='pages', verbose_name=_('script'), blank=True, null=True)
    file = models.FileField(_('Page file'), upload_to='script_pages/%Y/%m/%d', blank=True)
    image = models.ImageField(_('Image file'), upload_to='script_pages/%Y/%m/%d', blank=True)
    number = models.IntegerField(_('number'))

    class Meta(MetaCore):
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class Script(BaseResource):

    author = models.ForeignKey(User, related_name="scripts", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    exam = models.ForeignKey('Exam', related_name="scripts", verbose_name=_('exam'), blank=True, null=True, on_delete=models.SET_NULL)
    file = models.FileField(_('PDF file'), upload_to='exams/%Y/%m/%d', blank=True)
    box_uuid  = models.CharField(_('Box UUID'), max_length='256', blank=True)
    box_session_key  = models.CharField(_('Box session key'), max_length='1024', blank=True)
    corrector = models.ForeignKey('Corrector', related_name="scripts", verbose_name=_('corrector'), blank=True, null=True, on_delete=models.SET_NULL)
    note = models.FloatField(_('note'), blank=True)
    comments = models.TextField(_('comments'), blank=True)
    status = models.IntegerField(_('status'), choices=SCRIPT_STATUS, default=2, blank=True)
    reject_reason = models.IntegerField(_('reject_reason'), choices=REJECT_REASON, blank=True)
    date_corrected = models.DateTimeField(_('date corrected'), null=True, blank=True)

    class Meta(MetaCore):
        verbose_name = _('Script')
        verbose_name_plural = _('Scripts')


    def save(self, **kwargs):
        super(Script, self).save(**kwargs)
        if self.status == 3:
            self.date_corrected = self.date_modified
        if not self.corrector:
            self.auto_set_corrector()

    def auto_set_corrector(self):
        quota_list = []
        quotas = self.exam.course.quotas.all()
        for quota in quotas:
            if quota.value: 
                quota_list.append({'obj':quota, 'level': quota.level})
        lower_quota = sorted(quota_list, key=lambda k: k['level'])[0]
        self.corrector = lower_quota['obj'].corrector
        self.save()
    
    def make_from_pages(self):
        command = 'convert '
        all_pages = self.pages.all()
        num_pages = all_pages.count()
        pages = []
        paths = ''

        for page in all_pages:
            pages.append({'obj': page, 'number': page.number})
        
        pages = sorted(pages, key=lambda k: k['number'])
        
        for dict in pages:
            page = pages[dict]
            path = cache_path + os.sep + page.uuid + '.pdf'
            command = 'convert ' + page.file.path + ' -page A4 ' + path
            os.system(command)
            paths += ' ' + path

        output = script_path + os.sep + self.uuid + '.pdf'
        command = 'stapler ' + paths + ' ' + output
        os.system(command)
        self.file = output          
        self.save()

    def box_upload(self):
        import crocodoc
        crocodoc.api_token = settings.BOX_API_TOKEN
        file_handle = open(self.file.path, 'r')
        self.box_uuid = crocodoc.document.upload(file=file_handle)
        file_handle.close()
        user = {'id': self.corrector.id, 'name': self.corrector}
        self.box_admin_session_key = crocodoc.session.create(self.box_uuid, editable=True, user=user, 
                                filter='all', admin=True, downloadable=True,
                                copyprotected=False, demo=False, sidebar='visible')
        self.status = 2
        self.save()

    def get_box_admin_url(self):
        return 'https://crocodoc.com/view/' + self.box_session_key

    def get_box_user_url(self, user):
        user = {'id': user.id, 'name': user}
        session_key = crocodoc.session.create(self.box_uuid, editable=False, user=user, 
                                filter='all', admin=False, downloadable=True,
                                copyprotected=False, demo=False, sidebar='visible')
        return 'https://crocodoc.com/view/' + session_key


post_save.connect(set_file_properties, sender=Exam)
post_save.connect(set_file_properties, sender=Script)
post_save.connect(set_file_properties, sender=ScriptPage)
