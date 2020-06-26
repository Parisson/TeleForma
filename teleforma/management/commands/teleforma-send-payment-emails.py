# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import translation
from teleforma.models import *
import logging
import datetime

class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('teleforma')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Send emails to students that must pay"
    language_code = 'fr_FR'

    def email(self, student, kind, payment):
        site = Site.objects.get_current()
        ctx_dict = {'site': site, 'organization': settings.TELEFORMA_ORGANIZATION, 'student': student, 'payment': payment, 'period': student.period }
        subject_template = 'payment/email_%s_subject.txt' % kind
        message_template = 'payment/email_%s.txt' % kind
        subject = render_to_string(subject_template, ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string(message_template, ctx_dict)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.user.email], fail_silently=False)

    def handle(self, *args, **options):
        log_file = args[-1]
        period_name = args[-2]
        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')

        period = Period.objects.get(name=period_name)
        students = Student.objects.all()
        translation.activate(self.language_code)

        today = datetime.date.today()
        
        for student in students:
            if student.is_subscribed and student.user.email and student.period == period:
                for payment in student.payments.filter(type = 'online').exclude(online_paid = True).filter(scheduled__lte = today):
                    if payment.scheduled == today:
                        self.email(student, 'initial', payment)
                        logger.logger.info('initial email send for %s on %d' % (student.user.username, payment.id))
                    else:
                        delta = today - payment.scheduled
                        delta = delta.days
                        if delta % 7 == 0:
                            self.email(student, 'reminder', payment)
                            logger.logger.info('reminder email send for %s on %d' % (student.user.username, payment.id))

        logger.logger.info('############## Done #################')
