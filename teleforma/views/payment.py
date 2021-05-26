# -*- coding: utf-8 -*-

import datetime
import logging
import pprint
import subprocess

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from ..models.crfpa import Payment
from ..views.core import *

log = logging.getLogger('payment')


def call_scherlocks(what, data, merchant_id):
    """
    Perform a Scherlock's call, with parameters in data
    what is either 'request' or 'response', the program to call
    """
    log.info('call_scherlocks %r %r' % (what, data))
    requestbin = os.path.join(
        settings.PAYMENT_SHERLOCKS_PATH, 'bin/static', what)
    params = dict(data)
    params['pathfile'] = os.path.join(settings.PAYMENT_SHERLOCKS_PATH,
                                      'param/pathfile.' + merchant_id)
    params = ' '.join(['%s=%s' % (k, v) for k, v in params.items()])
    cmdline = requestbin + ' ' + params

    status, out = subprocess.getstatusoutput(cmdline)
    if status:
        raise OSError("error calling %s" % cmdline)
    res = out.split('!')[1:-1]
    if int(res[0]):
        raise ValueError("Scherlock's returned %s" % res[1])
    return res[2:]


def check_payment_info(data):
    """
    Check that the payment info are valid
    """
    response_code = data[8]
    cvv_response_code = data[14]

    log.info('check_payment_info %s %s' % (response_code, cvv_response_code))

    return response_code == '00'


def process_payment(request, payment):
    """
    Process a payment to Sherlocks
    """
    params = dict(settings.PAYMENT_PARAMETERS)
    period = payment.student.period
    period_short_name = period.name.split()[0]
    params['merchant_id'] = params['merchant_id'][period_short_name]
    merchant_id = params['merchant_id']
    params['amount'] = str(int(payment.value*100))
    params['order_id'] = str(payment.pk)
    current_site = get_current_site(request)
    root = 'https://%s' % (current_site.domain)

    kwargs = {'merchant_id': merchant_id}
    params['normal_return_url'] = root + reverse('teleforma-bank-success',
                                                 kwargs=kwargs)
    params['cancel_return_url'] = root + reverse('teleforma-bank-cancel',
                                                 kwargs=kwargs)
    params['automatic_response_url'] = root + reverse('teleforma-bank-auto',
                                                      kwargs=kwargs)
    pprint.pprint(params)
    res = call_scherlocks('request', params, merchant_id=merchant_id)
    return res[0]


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
        context['sherlock_info'] = process_payment(self.request, payment)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentStartView, self).dispatch(*args, **kwargs)


@csrf_exempt
def bank_auto(request, merchant_id):
    """
    Bank automatic callback
    """
    res = call_scherlocks('response', {'message': request.POST['DATA']},
                          merchant_id=merchant_id)
    order_id = res[24]
    payment = Payment.objects.get(pk=order_id)
    if check_payment_info(res) and payment.type == 'online' and not payment.online_paid:
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
    log.info("bank_success %r" % request.POST)
    res = call_scherlocks('response', {'message': request.POST['DATA']},
                          merchant_id=merchant_id)
    if check_payment_info(res):
        order_id = res[24]
        payment = Payment.objects.get(pk=order_id)
        if payment.type == 'online' and payment.online_paid and (payment.student.user_id == request.user.pk or request.user.is_superuser):
            return render_to_response('payment/payment_validate.html',
                                      {'payment': payment, },
                                      context_instance=RequestContext(request))
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
    return render_to_response('payment/payment_fail.html')
