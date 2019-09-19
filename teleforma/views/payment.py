# -*- coding: utf-8 -*-

from teleforma.models.crfpa import Payment, Student
from teleforma.models.core import Period
from teleforma.views.core import *
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError, PermissionDenied

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
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentStartView, self).dispatch(*args, **kwargs)

class PaymentValidateView(DetailView):

    template_name = 'payment/payment_validate.html'
    model = Payment

    def get_context_data(self, **kwargs):
        context = super(PaymentValidateView, self).get_context_data(**kwargs)
        payment = self.get_object()
        if payment.type != 'online' or payment.online_paid:
            raise PermissionDenied
        if payment.student.user_id != self.request.user.pk and not self.request.user.is_superuser:
            raise PermissionDenied

        payment.online_paid = True
        payment.save()
        context['payment'] = payment
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentValidateView, self).dispatch(*args, **kwargs)

