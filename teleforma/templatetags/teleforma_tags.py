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

import datetime
import json
import re
import urllib.parse as urlparse

from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.utils.encoding import force_text, smart_str
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from docutils.core import publish_parts

from ..exam.models import Quota, Script
from ..models.core import Document, Professor
from ..models.crfpa import IEJ, Course, NewsItem, Training
from ..views import get_courses

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


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


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
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return dictionary[key]


@register.filter
def from_course_type(contents, type):
    if contents:
        return contents.filter(course_type=type)


@register.filter
def streaming_only(contents):
    if contents:
        return contents.filter(streaming=True)


@register.filter
def from_doc_type(contents, type):
    if contents:
        return contents.filter(type=type)


@register.filter
def from_period(contents, period):
    if contents:
        if type(contents[0]) == Document:
            return contents.filter(periods__in=(period,))
        else:
            return contents.filter(period=period)


@register.simple_tag
def get_all_professors():
    return Professor.objects.all()


@register.simple_tag
def get_all_professors_with_courses():
    professors = []
    for professor in Professor.objects.order_by('user__last_name').all():
        name = professor.user.last_name + professor.user.first_name
        if name:
            professors.append({
                'username': professor.user.username,
                'name': professor.user.last_name + " " + professor.user.first_name,
                'courses': json.dumps([course.id for course in professor.courses.all()])
            })
    return professors


@register.simple_tag
def get_all_correctors_with_courses():
    correctors = {}

    for quota in Quota.objects.all():
        if not quota.corrector:
            continue
        if quota.corrector not in correctors:
            correctors[quota.corrector] = set()
        correctors[quota.corrector].add(quota.course.id)

    result = []
    for corrector in correctors.keys():
        name = corrector.last_name + corrector.first_name
        if name:
            result.append({
                'id': corrector.id,
                'username': corrector.username,
                'name': corrector.last_name + " " + corrector.first_name,
                'courses': json.dumps(list(correctors[corrector]))
            })
    result = sorted(result, key=lambda corrector: int(corrector['id']))
    return result


@register.simple_tag
def get_all_admins():
    return User.objects.filter(is_superuser=True).order_by('last_name')


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


@register.simple_tag
def show_chat(user):
    """ everybody should see the chat panel, except the correctors """
    professor = user.professor.all()
    if user.is_superuser or professor:
        return True
    if user.quotas.all():
        return False
    return True


@register.filter
def get_audio_id(media):
    for m in media.transcoded.all():
        if 'audio' in m.mime_type:
            return m.id
    return


@register.filter
def get_video_id(media):
    if media.conference:
        medias = media.conference.media.all()
        for m in medias:
            if 'video' in m.mime_type:
                return m.id
    return


@register.filter
def get_host(url, host):
    u = urlparse(url)
    if host == '127.0.0.1' or host == 'localhost':
        nu = u.scheme + '://' + host + ':' + str(u.port) + u.path
        return nu
    else:
        return url


@register.filter
def published(doc):
    if doc:
        return doc.filter(is_published=True)


def scripts_count(user, period, statuses):
    if not period:
        return ''
    Q1 = Q(author=user)
    Q2 = Q(corrector=user)
    scripts = Script.objects.filter(Q1 | Q2).filter(status__in=statuses,
                                                    period=period)
    if scripts:
        return ' (' + str(len(scripts)) + ')'
    else:
        return ''


@register.simple_tag
def untreated_scripts_count(user, period):
    return scripts_count(user, period, (3,))


@register.simple_tag
def treated_scripts_count(user, period):
    return scripts_count(user, period, (4,))


@register.simple_tag
def get_training_profile(user):
    text = ''
    if user:
        student = user.student.all()
        if student:
            student = student[0]
            if student.platform_only:
                text += 'Internaute - '
            for training in student.trainings.all():
                text += str(training) + ' '
    return text


@register.inclusion_tag('teleforma/inc/newsitems_portlet.html', takes_context=True)
def newsitems_portlet(context, course_id, period_id):
    request = context['request']
    user = request.user

    def get_data(newsitem):
        return {
            'id': newsitem.id,
            'title': newsitem.title,
            'text': newsitem.text,
            'creator': newsitem.creator,
            'created': newsitem.created,
            'can_edit': newsitem.can_edit(request),
            'can_delete': newsitem.can_delete(request),
        }

    course = get_object_or_404(Course, id=course_id)
    course_newsitems = [get_data(news) for news in NewsItem.objects.filter(
        deleted=False, course__id=course_id, period_id=period_id).order_by('-created')]
    all_newsitems = [get_data(news) for news in NewsItem.objects.filter(
        deleted=False, period_id=period_id).order_by('-created')]
    can_add = False
    if user.is_staff or user.professor.count():
        can_add = True
    return {
        'can_add': can_add,
        'course': course,
        'period_id': period_id,
        'course_newsitems': course_newsitems,
        'all_newsitems': all_newsitems
    }


##### FROM TELEMETA #####

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
        match = re.match(
            '^(\.\. *(?:_[^:]*:|(?:\|\w+\|)? *image::) *)([^ ]+) *$', line)
        if match:
            directive, urlname = match.groups()
            line = directive
            try:
                i = urlname.index('telemeta-')
            except ValueError:
                i = -1
            if i == 0:
                line += reverse(urlname)
            elif urlname[:1] != '/':
                line += reverse('telemeta-flatpage',
                                args=[path + '/../' + urlname])
            else:
                line += urlname

        parsed += line + "\n"

    parts = publish_parts(source=smart_str(
        parsed), writer_name="html4css1", settings_overrides={})
    return mark_safe('<div class="rst-content">\n' + force_text(parts["html_body"]) + '</div>')


render_flatpage.is_safe = True
