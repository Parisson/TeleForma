
from django import template
from django.utils.http import urlquote
from teleforma.models import *
from django.core.urlresolvers import reverse
from django.utils import html
from django import template
from django.utils.text import capfirst
from django.utils.translation import ungettext
from docutils.core import publish_parts
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django import db
import re
import os
import datetime
from django.conf import settings
from django.template.defaultfilters import stringfilter
import django.utils.timezone as timezone
from timezones.utils import localtime_for_timezone
from django.utils.translation import ugettext_lazy as _
from teleforma.views import get_courses

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
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
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
    return localtime_for_timezone(value, timezone)

@register.filter
def or_me(value, arg):
    """
    Replace the value by a fixed pattern, if it equals the argument.

    Typical usage: sender|or_me:user

    """
    if not isinstance(value, (unicode, str)):
        value = unicode(value)
    if not isinstance(arg, (unicode, str)):
        arg = unicode(arg)
    return _('me') if value == arg else value

@register.filter
def yes_no(bool):
    if bool:
        return _('Yes')
    else:
        return _('No')
