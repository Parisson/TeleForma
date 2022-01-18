# -*- coding: utf-8 -*-

from django import template
from ..models.core import Period

register = template.Library()

@register.inclusion_tag('admin/webclass/webclassrecord/add_records_links.html', takes_context=True)
def add_records_links(context):

    periods = Period.objects.filter(is_open=True)
    return {
        'periods':periods,
    }


@register.inclusion_tag('webclass/webclass_record.html', takes_context=True)
def webclass_record(context, record):
    return {
        'record':record
    }
