# -*- coding: utf-8 -*-

from django import template
from teleforma.models.crfpa import Period

register = template.Library()

@register.inclusion_tag('admin/webclass/webclassrecord/add_records_links.html', takes_context=True)
def add_records_links(context):

    periods = Period.objects.filter(is_open=True)
    return {
        'periods':periods,
    }
