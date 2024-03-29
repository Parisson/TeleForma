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

from __future__ import division

import datetime
import mimetypes
import os
from teleforma.utils import guess_mimetypes
import urllib
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from postman.models import Message
from postman.utils import notify_user
from teleforma.models.core import Course, Period

from ..models.core import session_choices

app = 'teleforma'


class MetaCore:

    app_label = 'exam'


# import boxsdk
# from boxsdk import OAuth2, Client
# import StringIO
#
# box_client_id = settings.BOX_CLIENT_ID
# box_client_secret = settings.BOX_CLIENT_SECRET
# box_redirect_url = settings.BOX_REDIRECT_URL
#
# oauth = OAuth2(
#     client_id=box_client_id,
#     client_secret=box_client_secret,
#     store_tokens='',
# )
#
# box_auth_url, box_csrf_token = oauth.get_authorization_url('http://' + BOX_REDIRECT_URL)
# box_client = Client(oauth)

SCRIPT_STATUS = ((0, _('rejected')), (1, _('draft')), (2, _('submitted')),
                 (3, _('pending')), (4, _('marked')), (5, _('read')),
                 (6, _('backup')), (7, _('stat')))

REJECT_REASON = (('unreadable', _('unreadable')),
                 ('bad orientation', _('bad orientation')),
                 ('bad framing', _('bad framing')),
                 ('incomplete', _('incomplete')),
                 ('wrong course', _('wrong course')),
                 ('duplicate', _('duplicate')),
                 ('other', _('other')),
                 ('wrong format', _('wrong format')),
                 ('unreadable file', _('unreadable file')),
                 ('no file', _('no file')),
                 ('error retrieving file', _('error retrieving file')),
                 ('file too large', _('file too large')),
                 )

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

    course = models.ForeignKey(Course, related_name="quotas", verbose_name=_(
        'course'), null=True, blank=True, on_delete=models.SET_NULL)
    corrector = models.ForeignKey(User, related_name="quotas", verbose_name=_(
        'corrector'), null=True, blank=False, on_delete=models.SET_NULL)
    period = models.ForeignKey(Period, related_name='quotas', verbose_name=_(
        'period'), null=True, blank=True, on_delete=models.SET_NULL)
    session = models.CharField(
        _('session'), choices=session_choices, max_length=16, default="1")
    value = models.IntegerField(_('value'))
    date_start = models.DateField(_('date start'))
    date_end = models.DateField(_('date end'))
    script_type = models.ForeignKey('ScriptType', related_name='quotas', verbose_name=_(
        'type'), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta(MetaCore):
        verbose_name = _('Quota')
        verbose_name_plural = _('Quotas')
        ordering = ['-date_end']

    def __str__(self):
        title = ' - '.join([str(self.corrector), self.course.title,
                            str(self.all_script_count) + '/' + str(self.value)])
        if self.script_type:
            title = ' - '.join([title, str(self.script_type)])
        if self.date_start:
            title = ' - '.join([title, str(self.date_start)])
        if self.date_end:
            title = ' - '.join([title, str(self.date_end)])
        return title

    def script_count(self, statuses):
        if self.corrector:
            q = self.corrector.corrector_scripts.filter(status__in=statuses)
            q = q.filter(course=self.course)
            q = q.filter(period=self.period)
            q = q.filter(session=self.session)
            # Careful, MySQL considers '2019-07-28 11:42:00" to not be >= "2019-07-28"
            start = self.date_start
            end = self.date_end + datetime.timedelta(days=1)
            q = q.filter(date_submitted__gte=start).filter(
                date_submitted__lte=end)
            return q.count()
        else:
            return 0

    @property
    def all_script_count(self):
        return self.script_count(statuses=(3, 4, 5))

    @property
    def pending_script_count(self):
        return self.script_count(statuses=(3,))

    @property
    def marked_script_count(self):
        return self.script_count(statuses=(4, 5))

    @property
    def level(self):
        if self.value:
            if self.value != 0:
                level = 100*self.all_script_count/self.value
                return round(level, 2)
            else:
                return 0
        else:
            return 0


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(
        _('date modified'), auto_now=True, null=True)
    uuid = models.CharField(_('UUID'), blank=True, max_length=512)
    mime_type = models.CharField(
        _('MIME type'), max_length=128, blank=True, null=True)
    sha1 = models.CharField(_('sha1'), blank=True, max_length=512)

    class Meta(MetaCore):
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(BaseResource, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)


class ScriptPage(BaseResource):

    script = models.ForeignKey('Script', related_name='pages', verbose_name=_(
        'script'), blank=True, null=True, on_delete=models.SET_NULL)
    file = models.FileField(
        _('Page file'), upload_to='script_pages/%Y/%m/%d', max_length=1024, blank=True)
    image = models.ImageField(
        _('Image file'), upload_to='script_pages/%Y/%m/%d', blank=True)
    rank = models.IntegerField(_('rank'), blank=True, null=True)

    class Meta(MetaCore):
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class ScriptType(models.Model):

    name = models.CharField(_('name'), max_length=512, blank=True)

    class Meta:
        verbose_name = _('ScriptType')
        verbose_name_plural = _('ScriptTypes')

    def __str__(self):
        return self.name


class Script(BaseResource):

    course = models.ForeignKey(Course, related_name="scripts", verbose_name=_(
        'course'), null=True, on_delete=models.SET_NULL)
    period = models.ForeignKey(Period, related_name='scripts', verbose_name=_('period'),
                               null=True, blank=True, on_delete=models.SET_NULL)
    session = models.CharField(_('session'), max_length=16, default="1")
    type = models.ForeignKey(ScriptType, related_name='scripts', verbose_name=_(
        'type'), null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, related_name="author_scripts", verbose_name=_(
        'author'), null=True, blank=True, on_delete=models.SET_NULL)
    corrector = models.ForeignKey(User, related_name="corrector_scripts", verbose_name=_(
        'corrector'), blank=True, null=True, on_delete=models.SET_NULL)
    file = models.FileField(
        _('PDF file'), upload_to='scripts/%Y/%m/%d', max_length=1024, blank=True)
    box_uuid = models.CharField(_('Box UUID'), max_length=256, blank=True)
    score = models.FloatField(_('score'), blank=True,
                              null=True, help_text="/20")
    comments = models.TextField(_('comments'), blank=True)
    status = models.IntegerField(
        _('status'), choices=SCRIPT_STATUS, blank=True)
    reject_reason = models.CharField(
        _('reason'), choices=REJECT_REASON, max_length=256, blank=True)
    date_submitted = models.DateTimeField(
        _('date submitted'), null=True, blank=True)
    date_marked = models.DateTimeField(_('date marked'), null=True, blank=True)
    date_rejected = models.DateTimeField(
        _('date rejected'), null=True, blank=True)
    url = models.CharField(_('URL'), max_length=2048, blank=True)

    @property
    def title(self):
        if self.type and self.course:
            title = [self.course.title, self.type.name, _(
                "Session") + ' ' + self.session, str(self.date_added)]
        elif self.course:
            title = [self.course.title, _(
                "Session") + ' ' + self.session, str(self.date_added)]
        else:
            title = [self.session, str(self.date_added)]
        if self.author:
            title.append(str(self.author.first_name) +
                        ' ' + str(self.author.last_name))
        return ' - '.join(title)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        period_id = None
        if self.period:
            period_id = self.period.id
        return reverse_lazy('teleforma-exam-script-detail',
                            kwargs={'pk': self.id, 'period_id': period_id})

    class Meta(MetaCore):
        verbose_name = _('Script')
        verbose_name_plural = _('Scripts')
        ordering = ['date_added']

    def auto_set_corrector(self):

        self.date_submitted = datetime.datetime.now()

        quota_list = []
        all_quotas = self.course.quotas.filter(date_start__lte=self.date_submitted,
                                               date_end__gte=self.date_submitted,
                                               session=self.session,
                                               period=self.period)

        # Commented to not filter by type anymore
        # quotas = all_quotas.filter(script_type=self.type)
        # if not quotas:
        #     quotas = all_quotas.filter(script_type=None)

        quotas = all_quotas

        if quotas:
            for quota in quotas:
                if quota.value:
                    quota_list.append({'obj': quota, 'level': quota.level})
            lower_quota = sorted(quota_list, key=lambda k: k['level'])[0]
            self.corrector = lower_quota['obj'].corrector
        else:
            # FIXME: default corrector goes to settings
            self.corrector = User.objects.filter(is_superuser=True)[1]

        self.status = 3
        # self.save()

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
        if not self.file and self.score:
            self.status = 7
        elif self.status == 4 and self.score:
            self.mark()
        elif self.status == 0 and self.reject_reason:
            self.reject()
        # HOTFIX
        if not self.mime_type:
            self.mime_type = 'application/pdf'
        super(Script, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super(Script, self).save(*args, **kwargs)

    def uuid_link(self):
        old_abs = self.file.path
        old_abs_list = old_abs.split(os.sep)
        old_abs_root = old_abs_list[:-1]

        old_rel = str(self.file)
        old_rel_list = old_rel.split(os.sep)
        old_rel_root = old_rel_list[:-1]

        filename, ext = os.path.splitext(old_abs_list[-1])

        new_abs = os.sep.join(old_abs_root) + os.sep + str(self.uuid) + ext
        new_rel = os.sep.join(old_rel_root) + os.sep + str(self.uuid) + ext

        if not os.path.exists(new_abs):
            os.symlink(filename + ext, new_abs)

        if not self.url:
            self.url = settings.MEDIA_URL + str(new_rel)

    @property
    def safe_url(self):
        domain = Site.objects.get_current().domain
        url = self.url
        url = url.replace(
            'http://e-learning.crfpa.pre-barreau.com', '//' + domain)
        return urllib.quote(url)

    def unquoted_url(self):
        domain = Site.objects.get_current().domain
        url = self.url
        url = url.replace(
            'http://e-learning.crfpa.pre-barreau.com', '//' + domain)
        return url

    def has_annotations_file(self):
        """
        check if an annotations file exists. Then use this file, otherwise use the new db implementation
        """
        return os.path.exists(os.path.join(settings.WEBVIEWER_ANNOTATIONS_PATH, self.uuid+'.xfdf'))

    def auto_reject(self, mess):
        self.reject_reason = mess
        self.status = 0
        self.corrector = User.objects.filter(is_superuser=True)[1]
        self.reject()
        # self.save()

    def submit(self):
        self.box_upload_done = 0

        if not self.file:
            self.auto_reject('no file')
            return

        if not os.path.exists(self.file.path):
            self.auto_reject('file not found')
            return

        mime_type = guess_mimetypes(self.file.path)
        if mime_type:
            if not 'pdf' in mime_type:
                self.auto_reject('wrong format')
                return
        else:
            self.auto_reject('wrong format')
            return

        if os.stat(self.file.path).st_size > settings.TELEFORMA_EXAM_SCRIPT_MAX_SIZE:
            self.auto_reject('file too large')
            return

        if not self.status == 0 and self.file:
            # if not self.box_uuid:
            #     self.uuid_link()
            # self.box_upload()
            if not self.corrector:
                self.auto_set_corrector()

    def mark(self):
        self.date_marked = datetime.datetime.now()
        site = Site.objects.all()[0]
        context = {'script': self, 'site': site}
        text = render_to_string('exam/messages/script_marked.txt', context)
        a = ugettext('Script')
        v = ugettext('marked')
        subject = '%s %s' % (a, v)
        mess = Message(sender=self.corrector, recipient=self.author,
                       subject=subject[:119], body=text)
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
        mess = Message(sender=self.corrector, recipient=self.author,
                       subject=subject[:119], body=text)
        mess.moderation_status = 'a'
        mess.save()
        notify_user(mess, 'acceptance', site)


def set_file_properties(sender, instance, **kwargs):
    if instance.file:
        trig_save = False
        if not instance.mime_type:
            mime_type = guess_mimetypes(instance.file.path)
            if mime_type:
                instance.mime_type = guess_mimetypes(instance.file.path)
                trig_save = True
            # HOTFIX
            else:
                instance.mime_type = 'application/pdf'
        if not instance.sha1:
            instance.sha1 = sha1sum_file(instance.file.path)
            trig_save = True
        if not instance.url:
            instance.uuid_link()
            trig_save = True
        if not instance.corrector:
            instance.submit()
            trig_save = True
        if trig_save:
            super(sender, instance).save()

        # if hasattr(instance, 'image'):
        #     if not instance.image:
        #         path = cache_path + os.sep + instance.uuid + '.jpg'
        #         command = 'convert ' + instance.file.path + ' ' + path
        #         os.system(command)
        #         instance.image = path


post_save.connect(set_file_properties, sender=Script,
                  dispatch_uid="script_post_save")
post_save.connect(set_file_properties, sender=ScriptPage,
                  dispatch_uid="scriptpage_post_save")
