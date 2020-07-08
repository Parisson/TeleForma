# -*- coding: utf-8 -*-

from django import template
from datetime import date
from teleforma.models import Payment
register = template.Library()

@register.inclusion_tag('payment/payment_summary.html',
                        takes_context=True)
def payment_summary(context, payment, with_pending=True):
    student = payment.student
    objs = Payment.objects.filter(student = student)
    payments = []
    today = date.today()
    for obj in objs:
        if obj.type == 'online':
            if obj.online_paid:
                status = 'payé'
                sclass = "paid" 
            elif obj.id == payment.id and with_pending:
                status = 'en cours'
                sclass = "pending"
            elif obj.scheduled > today:
                status = 'à payer ultérieurement'
                sclass = "topay_later"
            else:
                status = 'à payer'
                sclass = "topay"
        else:
            status = obj.get_type_display()
            sclass = "offline"
        payments.append({ 'scheduled': obj.scheduled or obj.date_created.date(),
                          'sclass': sclass,
                          'value': obj.value,
                          'status': status })
    payments.sort(key = lambda p: p['scheduled'])
   
    return { "payments": payments,
             "student": student,
             "user": student.user }

@register.filter
def payment_format_amount(value):
    if value is None:
        return ""
    value = '%.2f' % float(value)
    unit, decimal = value.split('.')    
    res = ''
    if unit.startswith('-'):
        prefix = '-'
        unit = unit[1:]
    else:
        prefix = ''
    while len(unit) > 3:
        res = res + ' ' + unit[-3:]
        unit = unit[:-3]
    res = prefix + unit + res
    return '%s,%s' % (res, decimal)
