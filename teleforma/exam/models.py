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

import os, uuid, time, hashlib, mimetypes, tempfile, datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Max, Min
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.defaultfilters import slugify

from teleforma.models import *
from django.template.loader import render_to_string
from postman.utils import email_visitor, notify_user
from postman.models import Message

app = 'teleforma'

class MetaCore:

    app_label = 'exam'

import crocodoc
crocodoc.api_token = settings.BOX_API_TOKEN

SCRIPT_STATUS = ((0, _('rejected')), (1, _('draft')), (2, _('submitted')),
                (3, _('pending')),(4, _('marked')), (5, _('read')) )

REJECT_REASON = (('unreadable', _('unreadable')),
                ('bad orientation', _('bad orientation')),
                ('bad framing', _('bad framing')),
                ('incomplete', _('incomplete')),)

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


class Quota(models.Model):

    course = models.ForeignKey(Course, related_name="quotas", verbose_name=_('course'), blank=True, null=True)
    corrector = models.ForeignKey(User, related_name="quotas", verbose_name=_('corrector'), blank=True, null=True)
    period = models.ForeignKey(Period, related_name='quotas', verbose_name=_('period'),
                                 null=True, blank=True, on_delete=models.SET_NULL)
    value = models.IntegerField(_('value'))
    date_start = models.DateField(_('date start'))
    date_end = models.DateField(_('date end'))

    class Meta(MetaCore):
        verbose_name = _('Quota')
        verbose_name_plural = _('Quotas')
        ordering = ['date_start']

    def __unicode__(self):
        return ' - '.join([unicode(self.corrector), self.course.title, str(self.value)])

    @property
    def level(self):
        if self.value:
            if self.value != 0:
                level = 100*self.corrector.corrector_scripts.filter(Q(status=2) | Q(status=3) | Q(status=4) | Q(status=5)).count()/self.value
                return level
            else:
                return 0
        else:
            return 0


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True, null=True)
    uuid = models.CharField(_('UUID'), blank=True, max_length=512)
    mime_type = models.CharField(_('MIME type'), max_length=128, blank=True)
    sha1 = models.CharField(_('sha1'), blank=True, max_length=512)

    class Meta(MetaCore):
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(BaseResource, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.uuid)


class ScriptPage(BaseResource):

    script = models.ForeignKey('Script', related_name='pages', verbose_name=_('script'), blank=True, null=True)
    file = models.FileField(_('Page file'), upload_to='script_pages/%Y/%m/%d', blank=True)
    image = models.ImageField(_('Image file'), upload_to='script_pages/%Y/%m/%d', blank=True)
    rank = models.IntegerField(_('rank'), blank=True, null=True)

    class Meta(MetaCore):
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class ScriptType(models.Model):

    name  = models.CharField(_('name'), max_length='512', blank=True)

    class Meta:
        verbose_name = _('ScriptType')
        verbose_name_plural = _('ScriptTypes')

    def __unicode__(self):
        return self.name


class Script(BaseResource):

    course = models.ForeignKey(Course, related_name="scripts", verbose_name=_('course'), null=True, on_delete=models.SET_NULL)
    period = models.ForeignKey(Period, related_name='scripts', verbose_name=_('period'),
                                 null=True, blank=True, on_delete=models.SET_NULL)
    session = models.CharField(_('session'), choices=session_choices,
                                      max_length=16, default="1")
    type = models.ForeignKey(ScriptType, related_name='scripts', verbose_name=_('type'), null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, related_name="author_scripts", verbose_name=_('author'), null=True, blank=True, on_delete=models.SET_NULL)
    corrector = models.ForeignKey(User, related_name="corrector_scripts", verbose_name=_('corrector'), blank=True, null=True, on_delete=models.SET_NULL)
    file = models.FileField(_('PDF file'), upload_to='scripts/%Y/%m/%d', blank=True)
    box_uuid  = models.CharField(_('Box UUID'), max_length='256', blank=True)
    score = models.FloatField(_('score'), blank=True, null=True)
    comments = models.TextField(_('comments'), blank=True)
    status = models.IntegerField(_('status'), choices=SCRIPT_STATUS, blank=True)
    reject_reason = models.CharField(_('reason'), choices=REJECT_REASON, max_length='256', blank=True)
    date_submitted = models.DateTimeField(_('date submitted'), null=True, blank=True)
    date_marked = models.DateTimeField(_('date marked'), null=True, blank=True)
    date_rejected = models.DateTimeField(_('date rejected'), null=True, blank=True)
    url  = models.CharField(_('URL'), max_length='2048', blank=True)

    @property
    def title(self):
        return ' - '.join([self.course.title, self.type.name, _("Session") + ' ' + self.session,
                        unicode(self.author.first_name) + ' ' + unicode(self.author.last_name),
                        unicode(self.date_added)])

    def __unicode__(self):
        return unicode(self.title)

    class Meta(MetaCore):
        verbose_name = _('Script')
        verbose_name_plural = _('Scripts')
        ordering = ['-date_added']

    @property
    def box_admin_url(self):
        user = {'id': self.corrector.id, 'name': unicode(self.corrector)}
        session_key = crocodoc.session.create(self.box_uuid, editable=True, user=user,
                                filter='all', admin=True, downloadable=True,
                                copyprotected=False, demo=False, sidebar='invisible')
        return 'https://crocodoc.com/view/' + session_key

    @property
    def box_user_url(self):
        user = {'id': 2, 'name': 'Pierre Durand'}
        session_key = crocodoc.session.create(self.box_uuid, editable=False, user=user,
                                filter='all', admin=False, downloadable=True,
                                copyprotected=False, demo=False, sidebar='invisible')
        return 'https://crocodoc.com/view/' + session_key

    def auto_set_corrector(self):
        quota_list = []
        quotas = self.course.quotas.filter(date_start__lte=self.date_submitted,
                                            date_end__gte=self.date_submitted)
        if quotas:
            for quota in quotas:
                if quota.value:
                    quota_list.append({'obj':quota, 'level': quota.level})
            lower_quota = sorted(quota_list, key=lambda k: k['level'])[0]
            self.corrector = lower_quota['obj'].corrector
        else:
            self.corrector = User.objects.filter(is_superuser=True)[0]
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

    def save(self, *args, **kwargs):
        if self.status == 4 and self.score:
            self.mark()
        if self.status == 0 and self.reject_reason:
            self.reject()
        super(Script, self).save(*args, **kwargs)

    def fix_filename(self):
        old = self.file.path
        old_list = old.split(os.sep)
        path = old_list[:-1]
        filename, ext = os.path.splitext(old_list[-1])
        new = os.sep.join(path) + os.sep + slugify(filename) + ext
        os.rename(old, new)
        self.file.path = new
        self.save()

    def submit(self):
        self.date_submitted = datetime.datetime.now()
        # self.url = 'http://teleforma.parisson.com/media/scripts/2014/06/24/Gstreamer_monitoring_Pipleline.pdf'
        self.url = settings.MEDIA_URL + unicode(self.file)
        print self.url
        self.box_uuid = crocodoc.document.upload(url=self.url)
        while True:
            statuses = crocodoc.document.status([self.box_uuid,])
            if (len(statuses) != 0):
                if (statuses[0].get('error') == None):
                    if statuses[0]['status'] == 'DONE':
                        break
                    else:
                        time.sleep(1)
                else:
                    print '  File #1 failed :('
                    print '  Error Message: ' + statuses[0]['error']
            else:
                print 'failed :('
                print '  Statuses were not returned.'

        if not self.corrector:
            self.auto_set_corrector()

        self.status = 3
        self.save()

    def mark(self):
        self.date_marked = datetime.datetime.now()
        site = Site.objects.all()[0]
        context = {'script': self, 'site': site}
        text = render_to_string('exam/messages/script_marked.txt', context)
        a = ugettext('Script')
        v = ugettext('marked')
        subject = '%s %s' % (a, v)
        mess = Message(sender=self.corrector, recipient=self.author, subject=subject[:119], body=text)
        mess.moderation_status = 'a'
        mess.save()
        site = Site.objects.all()[0]
        notify_user(mess, 'acceptance', site)

    def reject(self):
        self.date_marked = datetime.datetime.now()
        self.date_rejected = datetime.datetime.now()
        site = Site.objects.all()[0]
        context = {'script': self, 'site': site}
        text = render_to_string('exam/messages/script_rejected.txt', context)
        a = ugettext('Script')
        v = ugettext('rejected')
        subject = '%s %s' % (a, v)
        mess = Message(sender=self.corrector, recipient=self.author, subject=subject[:119], body=text)
        mess.moderation_status = 'a'
        mess.save()
        notify_user(mess, 'acceptance', site)


def set_file_properties(sender, instance, **kwargs):
    if instance.file:
        if not instance.mime_type:
            instance.mime_type = mimetype_file(instance.file.path)
        if not instance.sha1:
            instance.sha1 = sha1sum_file(instance.file.path)
        if hasattr(instance, 'image'):
            if not instance.image:
                path = cache_path + os.sep + instance.uuid + '.jpg'
                command = 'convert ' + instance.file.path + ' ' + path
                os.system(command)
                instance.image = path


post_save.connect(set_file_properties, sender=Script, dispatch_uid="script_post_save")
post_save.connect(set_file_properties, sender=ScriptPage, dispatch_uid="scriptpage_post_save")
