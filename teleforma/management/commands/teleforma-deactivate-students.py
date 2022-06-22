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
    help = "Deactivate student user for a given period"
    language_code = 'fr_FR'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        log_file = args[-1]
        period_name = args[-2]

        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')

        period = Period.objects.get(name=period_name)
        students = Student.objects.filter(period=period)
        translation.activate(self.language_code)

        for student in students:
            if student.user:
                if student.is_subscribed and student.confirmation_sent and student.user.email and student.user.is_active:
                    student.user.is_active = False
                    student.user.save()
                    logger.logger.info('deactivated : ' + student.user.username)

        logger.logger.info('############## Done #################')
