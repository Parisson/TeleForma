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
    help = "Deactivate students accounts"
    language_code = 'fr_FR'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        log_file = args[-1]

        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')

        today = datetime.date.today()
        students = Student.objects.all()
        translation.activate(self.language_code)

        for student in students:
            #print(student)
            try:
                if student.user.email and student.user.is_active:
                    if student.period:
                        if student.period.date_close_accounts <= today:
                            student.user.is_active = False
                            student.user.save()
                            logger.logger.info('deactivated : ' + student.user.username)
                    else:
                        student.user.is_active = False
                        student.user.save()
                        logger.logger.info('deactivated : ' + student.user.username)
            except:
                continue

        logger.logger.info('############## Done #################')
