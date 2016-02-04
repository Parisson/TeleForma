from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from django.utils import translation
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
from postman import *


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
    help = "Send an email to new subscribed student"
    language_code = 'fr_FR'

    def email(self, student):
        site = Site.objects.get_current()
        if student.platform_only:
            mode = 'E-learning'
        else:
            mode = 'Presentielle'
        ctx_dict = {'site': site, 'organization': settings.TELEMETA_ORGANIZATION, 'student': student, 'mode': mode}
        subject_template = 'teleforma/messages/email_inscr_sujet.txt'
        message_template = 'teleforma/messages/email_inscription.txt'
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

        for student in students:
            if student.is_subscribed and not student.confirmation_sent and not student.user.is_active and student.user.email and student.period == period:
                self.email(student)
                student.confirmation_sent = True
                student.save()
                student.user.is_active = True
                student.user.save()
                logger.logger.info('email send : ' + student.user.username)

        logger.logger.info('############## Done #################')
