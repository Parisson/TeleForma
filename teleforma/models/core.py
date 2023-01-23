#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   teleforma

   Copyright (c) 2012-2017 Guillaume Pellerin <yomguy@parisson.com>

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

import datetime
import mimetypes
import os
import string
import random
import requests
import asyncio
from teleforma.utils import guess_mimetypes

import django.db.models as models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import InvalidPage
from django.db import models
from django.forms.fields import FileField
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
# from quiz.models import Quiz
from sorl.thumbnail import default as sorl_default

import httpx

from ..fields import ShortTextField

HAS_TELEMETA = False
if 'telemeta' in settings.INSTALLED_APPS:
    HAS_TELEMETA = True

app_label = 'teleforma'


def get_n_choices(n):
    return [(str(x), str(y)) for x in range(1, n) for y in range(1, n) if x == y]


def get_nint_choices(n):
    return [(x, y) for x in range(1, n) for y in range(1, n) if x == y]


session_choices = get_n_choices(settings.TELEFORMA_EXAM_MAX_SESSIONS+1)

server_choices = [('icecast', 'icecast'), ('stream-m', 'stream-m')]
streaming_choices = [('mp3', 'mp3'), ('ogg', 'ogg'),
                     ('webm', 'webm'), ('mp4', 'mp4')]
mimetypes.add_type('video/webm', '.webm')

ITEM_TRANSODING_STATUS = ((0, _('broken')), (1, _('pending')), (2, _('processing')),
                          (3, _('done')), (5, _('ready')))

payment_choices = [
    ('online', u'en ligne'),
    ('check', u'par chèque'),
    ('tranfer', u'par virement'),
    ('credit card', u'par carte'),
    ('money', u'en liquide'),
    ('other', u"autre"),
]

payment_schedule_choices = [
    ('split', u'en plusieurs fois'),
    ('once', u'en une seule fois'),
]

STATUS_CHOICES = (
    (0, _('Hidden')),
    (1, _('Private')),
    (2, _('Draft')),
    (3, _('Public')),
)

WEIGHT_CHOICES = get_nint_choices(5)


def get_random_hash():
    hash = random.getrandbits(128)
    return "%032x" % hash


def get_user_role(user):
    if user.is_superuser:
        return 'superuser'
    elif user.professor.exists():
        return 'professor'
    elif user.student.exists():
        return 'student'
    else:
        return 'corrector'


class MetaCore:
    app_label = app_label


class Organization(models.Model):

    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'organization'
        verbose_name = _('organization')


class Department(models.Model):

    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    organization = models.ForeignKey(
        'Organization', related_name='department', verbose_name=_('organization'), on_delete=models.CASCADE)
    domain = models.CharField(_('Master domain'), max_length=255, blank=True)
    default_period = models.ForeignKey('Period', related_name='departments', verbose_name=_(
        'period'), null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.__str__())

    class Meta(MetaCore):
        db_table = app_label + '_' + 'department'
        verbose_name = _('department')


class Period(models.Model):

    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    parent = models.ForeignKey('Period', related_name='children', verbose_name=_(
        'parent'), blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('Department', related_name='period',
                                   verbose_name=_('department'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    date_begin = models.DateField(_('begin date'), null=True, blank=True)
    date_end = models.DateField(_('end date'), null=True, blank=True)
    date_password_init = models.DateField(
        _("date d'init de mot de passe"), null=True, blank=True)
    message_platform = models.TextField(
        _('message pour internaute'), blank=True)
    message_local = models.TextField(
        _('message pour presentielle'), blank=True)
    is_open = models.BooleanField(_('is open'), default=True)
    date_exam_end = models.DateTimeField(
        _("date de fin d'examens"), null=True, blank=True)
    nb_script = models.IntegerField(
        _("nombre maximal de copies"), null=True, blank=True)
    date_close_accounts = models.DateField(
        "date de fermeture des comptes étudiants", null=True, blank=True)
    date_inscription_start = models.DateField(
        "date d'ouverture des inscriptions", null=True, blank=True)
    date_inscription_end = models.DateField(
        "date de fermeture des inscriptions", null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta(MetaCore):
        db_table = app_label + '_' + 'period'
        verbose_name = _('period')
        ordering = ['name']


class CourseType(models.Model):

    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'course_type'
        verbose_name = _('course type')
        ordering = ['order']

    def to_dict(self):
        dict = {'name': self.name,
                'description': self.description,
                }
        return dict

    def from_dict(self, data):
        self.name = data['name']
        self.description = data['description']
        self.save()


class Course(models.Model):

    department = models.ForeignKey('Department', related_name='course',
                                   verbose_name=_('department'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    code = models.CharField(_('code'), max_length=255)
    title_tweeter = models.CharField(_('tweeter title'), max_length=255)
    date_modified = models.DateTimeField(
        _('date modified'), auto_now=True, null=True)
    number = models.IntegerField(_('number'), blank=True, null=True)
    synthesis_note = models.BooleanField(_('synthesis note'))
    obligation = models.BooleanField(_('obligations'))
    magistral = models.BooleanField(_('magistral'))
    procedure = models.BooleanField(_('procedure'))
    written_speciality = models.BooleanField(_('written_speciality'))
    oral_speciality = models.BooleanField(_('oral_speciality'))
    oral_1 = models.BooleanField(_('oral_1'))
    oral_2 = models.BooleanField(_('oral_2'))
    has_exam_scripts = models.BooleanField(_("copies d'examen"), default=True)
    # quiz = models.ManyToManyField(
    #     Quiz, verbose_name=_('quiz'), blank=True, null=True)
    # last professor which received a student message on automatic mode
    last_professor_sent = models.ForeignKey(
        'Professor', blank=True, null=True, on_delete=models.SET_NULL)

    periods = models.ManyToManyField('Period', related_name="courses",
                                     verbose_name=u'Périodes associées',
                                     blank=True)

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return slugify(str(self.code))

    def to_dict(self):
        dict = {'organization': self.department.organization.name,
                'department': self.department.name,
                'title': self.title,
                'description': self.description,
                'code': self.code,
                'title_tweeter': self.title_tweeter,
                'number': str(self.number),
                }
        return dict

    def from_dict(self, data):
        organization, c = Organization.objects.get_or_create(
            name=data['organization'])
        self.department, c = Department.objects.get_or_create(
            name=data['department'], organization=organization)
        self.title = data['title']
        self.description = data['description']
        self.code = data['code']
        self.title_tweeter = data['title_tweeter']
        if data['number'] != 'None':
            self.number = int(data['number'])
        self.save()

    def is_for_period(self, period):
        """
        Check if it's available for given period
        """
        periods = [p['id'] for p in self.periods.values('id')]
        return not periods or period.id in periods

    class Meta(MetaCore):
        db_table = app_label + '_' + 'course'
        verbose_name = _('course')
        ordering = ['number']


class CourseGroup(models.Model):
    """(CourseGroup description)"""

    name = models.CharField(_('name'), max_length=255)
    courses = models.ManyToManyField(Course, related_name="course_groups", verbose_name=_('courses'),
                                     blank=True)

    def __str__(self):
        return u"CourseGroup"

    class Meta(MetaCore):
        db_table = app_label + '_' + 'course_group'
        verbose_name = _('course group')


class Professor(models.Model):

    user = models.ForeignKey(User, related_name='professor',
                             verbose_name=_('user'), unique=True, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', related_name="professor",
                                     verbose_name=_('courses'),
                                     blank=True)
    department = models.ForeignKey('Department', related_name='professor',
                                   verbose_name=_('department'),
                                   blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return self.user.last_name + ' ' + self.user.first_name[0] + '.'
        else:
            return self.user.username

    def to_json_dict(self):
        data = {'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'courses': [course.code for course in self.courses.all()],
                }
        return data

    def get_absolute_url(self):
        return reverse_lazy('teleforma-profile-detail', kwargs={'username': self.user.username})

    class Meta(MetaCore):
        db_table = app_label + '_' + 'professor'
        verbose_name = _('professor')
        ordering = ['user__last_name']


class Room(models.Model):

    organization = models.ForeignKey(
        'Organization', related_name='room', verbose_name=_('organization'), on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)

    def __str__(self):
        return self.organization.name + ' - ' + self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'room'
        verbose_name = _('room')


class ConferencePublication(models.Model):
    conference = models.ForeignKey('Conference', related_name='publications', verbose_name=_('conference'),
                                    on_delete=models.CASCADE)
    period = models.ForeignKey('Period', verbose_name=_('period'),
                               on_delete=models.CASCADE)
    date_publish = models.DateTimeField(_('publishing date'), null=True, blank=True)
    status = models.IntegerField(
        _('status'), choices=STATUS_CHOICES, default=2)
    notified = models.BooleanField(_('notified'), default=False)

class Conference(models.Model):

    public_id = models.CharField(_('public_id'), max_length=255, blank=True, unique=True)
    department = models.ForeignKey('Department', related_name='conference', verbose_name=_('department'),
                                   null=True, blank=True, on_delete=models.SET_NULL)
    period = models.ForeignKey('Period', related_name='conference', verbose_name=_('period'),
                               null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(
        'Course', related_name='conference', verbose_name=_('course'), on_delete=models.CASCADE)
    course_type = models.ForeignKey(
        'CourseType', related_name='conference', verbose_name=_('course type'), on_delete=models.CASCADE)
    professor = models.ForeignKey('Professor', related_name='conference', verbose_name=_('professor'),
                                  blank=True, null=True, on_delete=models.SET_NULL)
    session = models.CharField(_('session'), choices=session_choices,
                               max_length=16, default="1")
    room = models.ForeignKey('Room', related_name='conference', verbose_name=_('room'),
                             null=True, blank=True, on_delete=models.SET_NULL)
    comment = ShortTextField(_('comment'), max_length=255, blank=True)
    date_begin = models.DateTimeField(_('begin date'), null=True, blank=True)
    date_end = models.DateTimeField(_('end date'), null=True, blank=True)
    date_publish = models.DateTimeField(_('publishing date'), null=True, blank=True)
    readers = models.ManyToManyField(User, related_name="conference", verbose_name=_('readers'),
                                     blank=True)
    status = models.IntegerField(
        _('status'), choices=STATUS_CHOICES, default=2)
    streaming = models.BooleanField(_('streaming'), default=True)
    web_class_group = models.ForeignKey('WebClassGroup', related_name='conferences', verbose_name=_('web class group'),
                                        blank=True, null=True, on_delete=models.SET_NULL)
    notified = models.BooleanField(_('notified'), default=False)
    notified_live = models.BooleanField("Notifié live", default=False)

    @property
    def description(self):
        return str(self)

    @property
    def session_as_int(self):
        try:
            return int(self.session)
        except ValueError:
            return 0

    @property
    def duration(self):
        if self.date_end:
            return self.date_end.replace(microsecond=0) - \
                   self.date_begin.replace(microsecond=0)
        else:
            return None

    @property
    def slug(self):
        slug = '-'.join([self.course.department.slug,
                         self.course.slug,
                         self.course_type.name.lower()])
        return slug

    def __str__(self):
        date = self.date_begin

        if self.professor:
            list = [self.course.title,
                    self.course_type.name, self.session,
                    self.professor.user.first_name,
                    self.professor.user.last_name,
                    str(date)]
        else:
            list = [self.course.title,
                    self.course_type.name, self.session,
                    str(date)]
        return ' - '.join(list)

    async def notify_async(self):
        if self.streaming and not self.notified_live:
            # Notify live conferences by sending a signal to websocket.
            # This signal will be catched by the channel instance to notify students
            from teleforma.models.notification import notify
            if settings.DEBUG:
                requests.post(f"{settings.CHANNEL_URL}{reverse('teleforma-live-conference-notify')}", {'id': self.id})
            else:
                transport = httpx.HTTPTransport(uds=settings.CHANNEL_URL)
                async with httpx.AsyncClient(transport=transport) as client:
                    response = await client.post("http://localhost" + reverse('teleforma-live-conference-notify'),
                                            data={'id': self.id}, timeout=20.0)
                    assert response.status_code == 200

    def notify_sync(self):
        if self.streaming and not self.notified_live:
            # Notify live conferences by sending a signal to websocket.
            # This signal will be catched by the channel instance to notify students
            from teleforma.models.notification import notify
            if settings.DEBUG:
                requests.post(f"{settings.CHANNEL_URL}{reverse('teleforma-live-conference-notify')}", {'id': self.id})
            else:
                transport = httpx.HTTPTransport(uds=settings.CHANNEL_URL)
                with httpx.Client(transport=transport) as client:
                    response = client.post("http://localhost" + reverse('teleforma-live-conference-notify'),
                                            data={'id': self.id}, timeout=20.0)
                    assert response.status_code == 200

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = get_random_hash()
        self.course.save()
        self.notify_sync()
        if not self.notified_live:
            self.notified_live = True
        super(Conference, self).save(*args, **kwargs)

    def to_dict(self):
        dict = [{'id': 'public_id', 'value': self.public_id, 'class': '', 'label': 'public_id'},
                {'id': 'organization', 'value': self.course.department.organization,
                    'class': '', 'label': 'Organization'},
                {'id': 'department', 'value': self.course.department,
                    'class': '', 'label': 'Department'},
                {'id': 'period', 'value': self.period,
                    'class': '', 'label': 'Period'},
                {'id': 'professor', 'value': self.professor,
                    'class': '', 'label': 'Professor'},
                {'id': 'session', 'value': self.session,
                    'class': '', 'label': 'Session'},
                {'id': 'comment', 'value': self.comment,
                    'class': '', 'label': 'Comment'},
                ]
        return dict

    def to_json_dict(self):
        data = {'id': self.public_id,
                'course_code': self.course.code,
                'course_type': self.course_type.name,
                'department': self.department.name if self.department else 'None',
                'organization': self.department.organization.name if self.department else 'None',
                'professor_id': self.professor.user.username if self.professor else 'None',
                'period': self.period.name if self.period else 'None',
                'session': self.session if self.session else 'None',
                'comment': self.comment if self.comment else 'None',
                'streaming': self.streaming if self.streaming else 'False',
                'streams': [],
                'date_begin': self.date_begin.strftime('%Y %m %d %H %M %S') if self.date_begin else 'None',
                'date_end': self.date_end.strftime('%Y %m %d %H %M %S') if self.date_end else 'None',
                'web_class_group': self.web_class_group.name if self.web_class_group else 'None',
                }

        if self.room:
            data['room'] = self.room.name
            data['organization'] = self.room.organization.name

        streams = self.livestream.all()
        if streams:
            for stream in streams:
                data['streams'].append({'host': stream.server.host,
                                        'port': stream.server.port,
                                        'server_type': stream.server.type,
                                        'stream_type': stream.stream_type})
        return data

    def from_json_dict(self, data):
        self.public_id = data['id']
        self.course, c = Course.objects.get_or_create(code=data['course_code'])
        self.course_type, c = CourseType.objects.get_or_create(
            name=data['course_type'])

        if 'streaming' in data:
            if data['streaming'] == 'False':
                self.streaming = False
            else:
                self.streaming = True

        organization, c = Organization.objects.get_or_create(
            name=data['organization'])

        if data['department'] != 'None':
            self.department, c = Department.objects.get_or_create(name=data['department'],
                                                                  organization=organization)

        if data['professor_id'] != 'None':
            user, c = User.objects.get_or_create(username=data['professor_id'])
            self.professor, c = Professor.objects.get_or_create(user=user)
            if c:
                self.professor.courses.add(self.course)

        if data['period'] != 'None':
            self.period, c = Period.objects.get_or_create(name=data['period'])

        if data['session'] != 'None':
            self.session = data['session']

        if data['date_begin'] != 'None':
            dl = data['date_begin'].split(' ')
            self.date_begin = datetime.datetime(int(dl[0]), int(dl[1]), int(dl[2]),
                                                int(dl[3]), int(dl[4]), int(dl[5]))

        if data['date_end'] != 'None':
            dl = data['date_end'].split(' ')
            self.date_end = datetime.datetime(int(dl[0]), int(dl[1]), int(dl[2]),
                                              int(dl[3]), int(dl[4]), int(dl[5]))
        if data['comment'] != 'None':
            self.comment = data['comment']

        if 'room' in data.keys():
            self.room, c = Room.objects.get_or_create(name=data['room'],
                                                      organization=organization)

        if 'web_class_group' in data.keys():
            if data['web_class_group'] != 'None':
                self.web_class_group = WebClassGroup.objet.get(
                    name=data['web_class_group'])

    def video(self):
        """
        get media video
        """
        try:
            return self.media.get(type='mp4')
        except Media.DoesNotExist:
            try:
                return self.media.get(type='webm')
            except Media.DoesNotExist:
                pass
        return None

    def publication_info(self, period):
        """
        Get publication info according to period.
        """
        publication = self.publications.filter(period=period).first()
        if not publication and self.period == period:
            publication = self
        elif not publication:
            return None
        
        return {
            'status': publication.status,
            'published': publication.status == 3,
            'publication_date': publication.date_publish,
            'notified': publication.notified
        }
        

    class Meta(MetaCore):
        db_table = app_label + '_' + 'conference'
        verbose_name = _('conference')
        ordering = ['-date_begin']

        indexes = [
            models.Index(fields=['course', 'course_type', 'period', 'streaming', '-date_begin' ]),
         ]

class StreamingServer(models.Model):

    element_type = 'streamingserver'

    protocol = models.CharField(_('protocol'), max_length=16, blank=True)
    host = models.CharField(_('host'), max_length=255)
    port = models.CharField(_('port'), max_length=32)
    path = models.CharField(_('path'), max_length=256, blank=True)
    type = models.CharField(_('type'), choices=server_choices, max_length=32)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    source_password = models.CharField(_('source password'), max_length=32)
    admin_password = models.CharField(
        _('admin password'), max_length=32, blank=True)

    def __str__(self):
        return self.protocol + '://' + self.host + ':' + self.port + self.path + ' - ' + self.type

    class Meta(MetaCore):
        db_table = app_label + '_' + 'streaming_server'
        verbose_name = _('streaming server')


class LiveStream(models.Model):

    element_type = 'livestream'

    conference = models.ForeignKey('Conference', related_name='livestream',
                                   verbose_name=_('conference'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    server = models.ForeignKey('StreamingServer', related_name='livestream',
                               verbose_name=_('streaming server'), on_delete=models.CASCADE)
    stream_type = models.CharField(_('Streaming type'),
                                   choices=streaming_choices, max_length=32)
    streaming = models.BooleanField(_('streaming'))

    @property
    def slug(self):
        if self.conference:
            return self.conference.slug
        else:
            return 'None'

    @property
    def mount_point(self):
        # mount_point = self.server.type + '/'
        mount_point = ''
        if self.server.type == 'stream-m':
            mount_point += 'consume/' + self.slug
        else:
            mount_point += self.slug + '.' + self.stream_type
        return mount_point

    @property
    def snapshot_url(self):
        url = ''
        if self.server.type == 'stream-m':
            url = self.server.protocol + '://' + self.server.host + ':' + \
                self.server.port + self.server.path + \
                '/snapshot/' + self.slug
        return url

    @property
    def url(self):
        return self.server.protocol + '://' + self.server.host + ':' + self.server.port + \
                self.server.path + self.mount_point

    def __str__(self):
        if self.conference:
            return self.conference.description
        else:
            return self.slug

    class Meta(MetaCore):
        db_table = app_label + '_' + 'live_stream'
        verbose_name = _('live stream')


class MediaBase(models.Model):
    "Base media resource"

    title = models.CharField(_('title'), max_length=255, blank=True)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    credits = models.CharField(_('credits'), max_length=255, blank=True)
    date_added = models.DateTimeField(
        _('date added'), auto_now_add=True, null=True)
    date_modified = models.DateTimeField(
        _('date modified'), auto_now=True, null=True)
    code = models.CharField(_('code'), max_length=255, blank=True)
    is_published = models.BooleanField(_('published'))
    mime_type = models.CharField(_('mime type'), max_length=255, blank=True)
    weight = models.IntegerField(
        _('weight'), choices=WEIGHT_CHOICES, default=1, blank=True)

    def get_fields(self):
        return self._meta.fields

    class Meta(MetaCore):
        abstract = True


class DocumentType(models.Model):

    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(
        _('description'), max_length=255, blank=True)
    number = models.IntegerField(_('number'), blank=True, null=True)
    for_corrector = models.BooleanField('autorisé aux correcteurs',
                                        blank=True, null=False,
                                        default=False)

    def __str__(self):
        return self.name

    class Meta(MetaCore):
        db_table = app_label + '_' + 'document_type'
        verbose_name = _('document type')
        ordering = ['number']


class Document(MediaBase):

    element_type = 'document'

    course = models.ForeignKey(
        'Course', related_name='document', verbose_name=_('course'), on_delete=models.CASCADE)
    course_type = models.ManyToManyField('CourseType', related_name='document',
                                         verbose_name=_('course type'), blank=True)
    periods = models.ManyToManyField('Period', related_name='documents', verbose_name=_('periods'),
                                     blank=True)
    type = models.ForeignKey('DocumentType', related_name='document', verbose_name=_('type'),
                             blank=True, null=True, on_delete=models.SET_NULL)
    session = models.CharField(_('session'), choices=session_choices,
                               max_length=16, default="1")
    iej = models.ForeignKey('IEJ', related_name='document', verbose_name=_('iej'),
                            blank=True, null=True, on_delete=models.SET_NULL)
    is_annal = models.BooleanField(_('annal'))
    annal_year = models.IntegerField(_('year'), blank=True, null=True)
    file = models.FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename",
                            max_length=1024, blank=True)
    readers = models.ManyToManyField(User, related_name="document", verbose_name=_('readers'),
                                     blank=True)

    def is_image(self):
        is_url_image = False
        if self.url:
            url_types = ['.png', '.jpg', '.gif', '.jpeg']
            for type in url_types:
                if type in self.url or type.upper() in self.url:
                    is_url_image = True
        return 'image' in self.mime_type or is_url_image

    def set_mime_type(self):
        self.mime_type = guess_mimetypes(self.file.path)

    def __str__(self):
        types = ' - '.join([str(t) for t in self.course_type.all()])
        return ' - '.join([str(self.course), str(types), self.title, str(self.date_added)])

    def save(self, **kwargs):
        if not self.is_annal:
            self.course.save()
        self.set_mime_type()
        super(Document, self).save(**kwargs)

    class Meta(MetaCore):
        db_table = app_label + '_' + 'document'
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['course', 'is_published', '-date_added' ]),
         ]


class DocumentSimple(MediaBase):

    element_type = 'document_simple'

    period = models.ForeignKey('Period', related_name='document_simple', verbose_name=_('period'),
                               null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename",
                            max_length=1024, blank=True)
    readers = models.ManyToManyField(User, related_name="document_simple", verbose_name=_('readers'),
                                     blank=True)

    def is_image(self):
        is_url_image = False
        if self.url:
            url_types = ['.png', '.jpg', '.gif', '.jpeg']
            for type in url_types:
                if type in self.url or type.upper() in self.url:
                    is_url_image = True
        return 'image' in self.mime_type or is_url_image

    def set_mime_type(self):
        self.mime_type = guess_mimetypes(self.file.path)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super(DocumentSimple, self).save(**kwargs)
        self.set_mime_type()

    class Meta(MetaCore):
        db_table = app_label + '_' + 'document_simple'
        ordering = ['-date_added']


class MediaTranscoded(models.Model):
    "Item file transcoded"

    element_type = 'transcoded item'

    item = models.ForeignKey(
        'Media', related_name="transcoded", verbose_name=_('item'), on_delete=models.CASCADE)
    mimetype = models.CharField(_('mime_type'), max_length=255, blank=True)
    date_added = models.DateTimeField(_('date'), auto_now_add=True)
    status = models.IntegerField(
        _('status'), choices=ITEM_TRANSODING_STATUS, default=1)
    file = models.FileField(
        _('file'), upload_to='items/%Y/%m/%d', max_length=1024, blank=True)

    @property
    def mime_type(self):
        if not self.mimetype:
            if self.file:
                if os.path.exists(self.file.path):
                    self.mimetype = guess_mimetypes(self.file.path)
                    self.save()
                    return self.mimetype
                else:
                    return 'none'
            else:
                return 'none'
        else:
            return self.mimetype

    def __str__(self):
        if self.item.title:
            return self.item.title + ' - ' + self.mime_type
        else:
            return str(self.item.id) + ' - ' + self.mime_type

    class Meta(MetaCore):
        db_table = app_label + '_media_transcoded'


class Media(MediaBase):
    "Describe a media resource linked to a conference"

    element_type = 'media'

    conference = models.ForeignKey('Conference', related_name='media', verbose_name=_('conference'),
                                   blank=True, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('Course', related_name='media', verbose_name=_('course'),
                               blank=True, null=True, on_delete=models.SET_NULL)
    course_type = models.ForeignKey('CourseType', related_name='media', verbose_name=_('course type'),
                                    blank=True, null=True, on_delete=models.SET_NULL)
    period = models.ForeignKey('Period', related_name='media', verbose_name=_('period'),
                               null=True, blank=True, on_delete=models.SET_NULL)
    if HAS_TELEMETA:
        item = models.ForeignKey(MediaItem, related_name='media',
                                 verbose_name='item', blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(
        _('type'), choices=streaming_choices, max_length=32)
    readers = models.ManyToManyField(User, related_name="media", verbose_name=_('readers'),
                                     blank=True)
    file = models.FileField(
        _('file'), upload_to='items/%Y/%m/%d', max_length=1024, null=True, blank=False)
    poster_file = models.FileField(
        _('poster file'), upload_to='items/%Y/%m/%d', max_length=255, null=True, blank=False)

    def set_mime_type(self):
        if self.file:
            mime_type = guess_mimetypes(self.file.path)
            if mime_type == 'audio/mpeg':
                self.mime_type = 'audio/mp3'
            else:
                self.mime_type = mime_type
            self.save()

    def __str__(self):
        if self.course:
            if self.conference:
                return str(self.conference) + ' - ' + str(self.mime_type)
            else:
                return self.course.title + ' ' + self.course_type.name
        else:
            return str(self.file)

    def save(self, **kwargs):
        super(Media, self).save(**kwargs)
        if self.course:
            self.course.save()

    def poster_url(self, geometry='640'):
        url = ''
        if self.poster_file:
            url = sorl_default.backend.get_thumbnail(
                self.poster_file, geometry).url
        return url

    class Meta(MetaCore):
        db_table = app_label + '_' + 'media'
        ordering = ['-date_modified', '-conference__session',]
        indexes = [
            models.Index(fields=['course', 'course_type', 'period', 'is_published', '-date_modified' ]),
         ]


class NamePaginator(object):
    """Pagination for string-based objects"""

    def __init__(self, object_list, on=None, per_page=25):
        self.object_list = object_list
        self.count = len(object_list)
        self.pages = []

        # chunk up the objects so we don't need to iterate over the whole list for each letter
        chunks = {}

        for obj in self.object_list:
            if on:
                obj_str = getattr(obj, on).encode('utf8')
            else:
                obj_str = obj.encode('utf8')

            if len(obj_str):
                letter = str.upper(obj_str[0])
            else:
                letter = ''

            if letter not in chunks:
                chunks[letter] = []

            chunks[letter].append(obj)

        # the process for assigning objects to each page
        current_page = NamePage(self)

        for letter in string.ascii_uppercase:
            if letter not in chunks:
                current_page.add([], letter)
                continue

            # the items in object_list starting with this letter
            sub_list = chunks[letter]

            new_page_count = len(sub_list) + current_page.count
            # first, check to see if sub_list will fit or it needs to go onto a new page.
            # if assigning this list will cause the page to overflow...
            # and an underflow is closer to per_page than an overflow...
            # and the page isn't empty (which means len(sub_list) > per_page)...
            if new_page_count > per_page and \
                    abs(per_page - current_page.count) < abs(per_page - new_page_count) and \
                    current_page.count > 0:
                # make a new page
                self.pages.append(current_page)
                current_page = NamePage(self)

            current_page.add(sub_list, letter)

        # if we finished the for loop with a page that isn't empty, add it
        if current_page.count > 0:
            self.pages.append(current_page)

    def page(self, num):
        """Returns a Page object for the given 1-based page number."""
        if len(self.pages) == 0:
            return None
        elif num > 0 and num <= len(self.pages):
            return self.pages[num-1]
        else:
            raise InvalidPage

    @property
    def num_pages(self):
        """Returns the total number of pages"""
        return len(self.pages)


class NamePage(object):
    def __init__(self, paginator):
        self.paginator = paginator
        self.object_list = []
        self.letters = []

    @property
    def count(self):
        return len(self.object_list)

    @property
    def start_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else:
            return None

    @property
    def end_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else:
            return None

    @property
    def number(self):
        return self.paginator.pages.index(self) + 1

    def add(self, new_list, letter=None):
        if len(new_list) > 0:
            self.object_list = self.object_list + new_list
        if letter:
            self.letters.append(letter)

    def __repr__(self):
        if self.start_letter == self.end_letter:
            return self.start_letter
        else:
            return '%c-%c' % (self.start_letter, self.end_letter)


class WebClassGroup(models.Model):

    name = models.CharField(_('name'), max_length=255)
    iejs = models.ManyToManyField('IEJ', related_name="web_class_group", verbose_name=_('IEJ'),
                                  blank=True)

    class Meta(MetaCore):
        verbose_name = _('web class group')
        verbose_name_plural = _('web class group')
        ordering = ['name']

    def to_json_dict(self):
        data = {'name': self.name,
                'iejs': [iej.name for iej in self.iejs.all()],
                }
        return data
