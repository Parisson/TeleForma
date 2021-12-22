# -*- coding: utf-8 -*-
# Copyright (c) 2011-2012 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

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
#
# Authors: Guillaume Pellerin <yomguy@parisson.com>

from django import template
from teleforma.models import *
from django.urls import reverse
from django import template
from docutils.core import publish_parts
from django.utils.encoding import smart_str, force_text
from django.utils.safestring import mark_safe
import re
import os
import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse
from teleforma.models.crfpa import Course
from teleforma.views import get_courses
from teleforma.context_processors import *
from urllib.parse import urlparse

register = template.Library()

# more translations for template variables
title = _('General tweeter')
title = _('Local tweeter')

class TeleFormaVersionNode(template.Node):
    def render(self, context):
        from teleforma import __version__
        return __version__

@register.tag
def teleforma_version(parser, token):
    "Get TeleForma version number"
    return TeleFormaVersionNode()

@register.filter
def parse_urls(text):
    output = ''
    for block in text.split(' '):
        if 'http://' in block:
            output += '<a href="' + block + '">' + block + '</a>'
        else:
            output += block
    return output


@register.tag
def value_from_settings(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return ValueFromSettings(var)

class ValueFromSettings(template.Node):
    def __init__(self, var):
        self.arg = template.Variable(var)
    def render(self, context):
        return settings.__getattr__(str(self.arg))

@register.filter
def user_courses(user):
    return get_courses(user)

@register.filter
def to_recipients(users):
    list = []
    for user in users:
        list.append(user.username)
    return ':'.join(list)

@register.filter
def localtime(value, timezone):
    from timezones.utils import localtime_for_timezone
    return localtime_for_timezone(value, timezone)

@register.filter
def or_me(value, arg):
    """
    Replace the value by a fixed pattern, if it equals the argument.

    Typical usage: sender|or_me:user

    """
    if not isinstance(value, str):
        value = str(value)
    if not isinstance(arg, str):
        arg = str(arg)
    return _('me') if value == arg else value

@register.filter
def yes_no(bool):
    if bool:
        return _('Yes')
    else:
        return _('No')

@register.filter
def from_course_type(contents, type):
    if contents:
        return contents.filter(course_type=type)

@register.filter
def from_doc_type(contents, type):
    if contents:
        return contents.filter(type=type)

@register.filter
def from_periods(contents, periods):
    if contents:
        return contents.filter(period__in=periods)

@register.simple_tag
def get_all_professors():
    return Professor.objects.all().order_by('user__first_name')

@register.simple_tag
def get_all_admins():
    return User.objects.filter(is_superuser=True).order_by('first_name')

@register.simple_tag
def get_all_trainings():
    return Training.objects.all()

@register.simple_tag
def get_all_iejs():
    return IEJ.objects.all()

@register.simple_tag
def get_all_courses():
    return Course.objects.all()

@register.simple_tag
def get_telecaster():
    return 'telecaster' in settings.INSTALLED_APPS

@register.simple_tag
def get_googletools():
    return 'googletools' in settings.INSTALLED_APPS

@register.filter
def get_audio_id(media):
    medias = media.conference.media.all()
    for m in medias:
        if 'audio' in m.mime_type:
            return m.id
    return

@register.filter
def get_video_id(media):
    medias = media.conference.media.all()
    for m in medias:
        if 'video' in m.mime_type:
            return m.id
    return

@register.filter
def set_host(url, host):
    u = urlparse(url)
    if host == '127.0.0.1' or host == 'localhost':
        nu = u.scheme + '://' + host + ':' + str(u.port) + u.path
        return nu
    else:
        return url

@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)

@register.filter
def submitted(question, user):
    answers = Answer.objects.filter(question=question, user=user, status=3)
    if answers:
        return answers[0].date_submitted
    else:
        return ''

@register.filter
def saved(question, user):
    answers = Answer.objects.filter(question=question, user=user, status=2)
    if answers:
        return answers[0].date_submitted
    else:
        return ''

@register.filter
def validated(question, user):
    answers = Answer.objects.filter(question=question, user=user, status=3, validated=True)
    if answers:
        return answers[0].date_validated
    else:
        return ''

@register.filter
def quiz_validated(seminar, user):
    quiz = seminar.quiz
    startdate = seminar.date_added
    enddate = seminar.expiry_date
    validations = QuizValidation.objects.filter(quiz=quiz, user=user, validated=True,date_validated__range=[startdate, enddate])
    if validations:
        return validations[0].date_validated
    else:
        return ''

@register.filter
def summary(text, N):
    t = text[:N]
    if not ' ' in t:
        t = text[:N/2]
    return t + '...'

@register.filter
def progress(seminar, user):
    return seminar_progress(user, seminar)

@register.filter
def in_download_formats(file):
    ext = os.path.splitext(file)[1][1:]
    return ext in settings.TELEFORMA_DOWNLOAD_FORMATS

@register.filter
def user_seminars(user):
    return all_seminars(user)['all_seminars']

@register.filter
def free_first(qs):
    free_formats = ['webm', 'ogg']
    medias = []
    for media in qs:
        if 'webm' in media.mime_type or 'ogg' in media.mime_type:
            medias.insert(0, media)
        else:
            medias.append(media)
    return medias

@register.simple_tag
def admin_username():
    return settings.ADMIN_USERNAME

@register.filter
def hours(time):
    return str(int(str(time).split(':')[0]))

@register.filter
def point(time):
    return str(time)

@register.filter
def preview(related):
    media = related.filter(title='preview')
    if media:
        return media[0]
    else:
        return None

@register.filter
def fancy_duration(duration):
    time = ''
    d = str(duration).split(':')
    hours = int(d[0])
    minutes = int(d[1])
    if hours:
        time += str(hours) + 'h'
    if minutes<10:
        minutes = '0' + str(minutes)
    else:
        minutes = str(minutes)
    time +=  minutes + 'mn'
    return time

@register.filter
def fancy_duration_shop_like(duration):
    if not duration:
        return ""
    time = ''
    d = str(duration).split(':')
    hours = int(d[0])
    minutes = int(d[1])
    if hours:
        time += str(hours) + 'h'
    time += "%02d" % minutes
    return time
    
@register.filter
def fancy_seconds(seconds):
    time = ''
    hours = int(seconds / 3600)
    minutes_int = (seconds % 3600) / 60
    if hours:
        if minutes_int:
            time += str(hours) + 'h'
        else:
            time += str(hours) + ' heure'
            if hours > 1:
                time += 's'
    if minutes_int<10:
        minutes = '0' + str(minutes_int)
    else:
        minutes = str(minutes_int)
    if minutes_int == 0 and hours:
        pass
    elif not hours:
        time = minutes + ' minutes'
    else:
        time += minutes
    return time

@register.simple_tag
def untreated_answer_count():
    answers = Answer.objects.filter(treated=False, status=3)
    if answers:
        return ' (' + str(len(answers)) + ')'
    else:
        return ''

@register.filter
def integer(value):
    if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
        return int(value)
    else:
        return 0

@register.filter
def quiz_progress(progress):
    if progress:
        return int(progress[0]*100.0/progress[1])
    else:
        return 100

### FROM TELEMETA
@register.simple_tag
def description():
    return settings.TELEFORMA_DESCRIPTION

@register.simple_tag
def organization():
    return settings.TELEFORMA_ORGANIZATION

@register.simple_tag
def current_year():
    return datetime.datetime.now().strftime("%Y")

@register.filter
def render_flatpage(content):
    parsed = ""
    path = getattr(content, 'path', '')
    if isinstance(content, str):
        content = content.split("\n")

    for line in content:
        match = re.match('^(\.\. *(?:_[^:]*:|(?:\|\w+\|)? *image::) *)([^ ]+) *$', line)
        if match:
            directive, urlname = match.groups()
            line = directive
            try:
                i = urlname.index('teleforma-')
            except ValueError:
                i = -1
            if i == 0:
                line += reverse(urlname)
            elif urlname[:1] != '/':
                line += reverse('teleforma-flatpage', args=[path + '/../' + urlname])
            else:
                line += urlname

        parsed += line + "\n"

    parts = publish_parts(source=smart_str(parsed), writer_name="html4css1", settings_overrides={})
    return mark_safe('<div class="rst-content">\n' + force_text(parts["html_body"]) + '</div>')
render_flatpage.is_safe = True