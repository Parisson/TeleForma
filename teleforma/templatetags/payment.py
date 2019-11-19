# -*- coding: utf-8 -*-

from django import template
from datetime import date
from teleforma.models import Payment
register = template.Library()

@register.inclusion_tag('payment/payment_summary.html',
                        takes_context=True)
def payment_summary(context, payment):
    objs = Payment.objects.filter(student = payment.student)
    payments = []
    today = date.today()
    for obj in objs:
        if obj.type == 'online':
            if obj.online_paid:
                status = 'payé'
                sclass = "paid" 
            elif obj.id == payment.id:
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
                          'value': obj.value,
                          'status': status })
    payments.sort(key = lambda p: p['scheduled'])
   
    return { "payments": payments }
