# -*- coding: utf-8 -*-

import datetime
import logging
import os
import pprint
import hashlib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView

from ..models.crfpa import Payment

log = logging.getLogger('payment')


def compute_sherlocks_seal(data, key):
    """
    Compute the seal for Sherlock's
    """
    data = data.encode('utf-8')
    seal = hashlib.sha256(data + key.encode('utf-8')).hexdigest()
    return seal

def encode_sherlocks_data(params, key):
    """
    Encode data for Sherlock's
    """
    data = []
    for k, v in params.items():
        v = v.replace('|', '_').replace(',', '_').replace('=', '_')
        data.append('%s=%s' % (k, v))
    data = '|'.join(data)
    seal = compute_sherlocks_seal(data, key)
    return data, seal
    
def check_payment_info(post_data):
    """
    Check that the payment info are valid
    """
    seal = post_data.get('Seal', None)
    data = post_data.get('Data', None)
    keys = [ p['_key'] for p in settings.PAYMENT_PARAMETERS.values() ]

    if not seal or not data:
        log.warning('Missing seal or data')
        raise SuspiciousOperation('Missing data')

    for key in keys:
        wanted_seal = compute_sherlocks_seal(data, key)
        if seal == wanted_seal:
            break
    else:
        log.warning('Invalid seal')
        raise SuspiciousOperation('Invalid seal')

    words = data.split('|')
    values = {}
    for word in words:
        if "=" in word:
            key, value = word.split('=', 1)
            values[key] = value

    order_id = values.get('orderId', None)
    code = values.get('responseCode', None)
    if not order_id or not code:
        log.warning('Missing order_id or code')
        raise SuspiciousOperation('Missing value in data')
    
    res = { 'order_id': order_id,
            'valid': code == '00' }

    log.debug('check_payment_info %s %s' % (order_id, code))

    return res


def process_payment(request, payment):
    """
    Process a payment to Sherlocks
    """
    period = payment.student.period
    period_short_name = period.name.split()[0]
    params = dict(settings.PAYMENT_PARAMETERS[period_short_name])
    key = params.pop('_key')    
    merchant_id = params['merchantId']
    params['amount'] = str(int(payment.value*100))
    params['orderId'] = str(payment.pk)
    if settings.SHERLOKS_USE_TRANSACTION_ID:
        params['s10TransactionReference.s10TransactionId'] = '%06d' % payment.pk
    else:
        params['transactionReference'] = str(payment.pk)
    current_site = get_current_site(request)
    root = 'https://%s' % (current_site.domain)

    kwargs = {'merchant_id': merchant_id}
    params['normalReturnUrl'] = root + reverse('teleforma-bank-success',
                                               kwargs=kwargs)
    params['automaticResponseURL'] = root + reverse('teleforma-bank-auto',
                                                    kwargs=kwargs)
    data, seal = encode_sherlocks_data(params, key)
    return data, settings.SHERLOKS_URL, seal


class PaymentStartView(DetailView):

    template_name = 'payment/payment_start.html'
    model = Payment

    def get_context_data(self, **kwargs):
        context = super(PaymentStartView, self).get_context_data(**kwargs)
        payment = self.get_object()
        if payment.type != 'online' or payment.online_paid:
            raise PermissionDenied
        if payment.student.user_id != self.request.user.pk and not self.request.user.is_superuser:
            raise PermissionDenied
        context['payment'] = payment
        data, url, seal = process_payment(self.request, payment)
        context['sherlock_url'] = url
        context['sherlock_data'] = data
        context['sherlock_seal'] = seal
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentStartView, self).dispatch(*args, **kwargs)


@csrf_exempt
def bank_auto(request, merchant_id):
    """
    Bank automatic callback
    """
    log.info("bank_auto %r" % request.POST)
    info = check_payment_info(request.POST)
    order_id = info['order_id']
    payment = Payment.objects.get(pk=order_id)
    if info['valid'] and payment.type == 'online' and not payment.online_paid:
        payment.online_paid = True
        payment.date_paid = datetime.datetime.now()
        if payment.student.restricted:
            student = payment.student
            if student.period.date_close_accounts > datetime.date.today():
                student.restricted = False
            # send mail
            data = {
                'mfrom': settings.DEFAULT_FROM_EMAIL,
                'mto': payment.student.user.email,
                'student': payment.student
            }
            message = render_to_string(
                'teleforma/messages/email_account_activated.txt', data)
            send_mail("Inscription à la formation Pré-Barreau", message, data['mfrom'], [data['mto']],
                      fail_silently=False)
            student.save()

        payment.save()
        log.info('bank_auto validating order_id %s' % (order_id))
        tmpl_name = 'payment_ok'
        res = 'OK - Validated'
    else:
        log.info('bank_auto failing order_id %s' % (order_id))
        tmpl_name = 'payment_failed'
        res = 'OK - Cancelled'

    user = payment.student.user
    data = {'mfrom': settings.DEFAULT_FROM_EMAIL,
            'mto': user.email,
            'student': user,
            'amount': payment.value, }

    subject_template = 'payment/email_%s_subject.txt' % tmpl_name
    message_template = 'payment/email_%s.txt' % tmpl_name
    subject = render_to_string(subject_template, data)
    subject = ''.join(subject.splitlines())
    message = render_to_string(message_template, data)
    send_mail(subject, message, data['mfrom'], [data['mto']],
              fail_silently=True)

    return HttpResponse(res)


@csrf_exempt
def bank_success(request, merchant_id):
    """
    Bank success callback
    """
    log.info("bank_auto %r" % request.POST)
    info = check_payment_info(request.POST)
    order_id = info['order_id']
    if info['valid']:
        payment = Payment.objects.get(pk=order_id)
        if payment.type == 'online' and payment.online_paid:
            return render(request, 'payment/payment_validate.html',
                                      {'payment': payment, })
    return HttpResponseRedirect('/echec-de-paiement')


@csrf_exempt
def bank_cancel(request, merchant_id):
    """
    Bank cancel operation callback
    """
    return HttpResponseRedirect('/echec-de-paiement')


def bank_fail(request):
    """
    Display message when a payment failed
    """
    return render(request, 'payment/payment_fail.html')
