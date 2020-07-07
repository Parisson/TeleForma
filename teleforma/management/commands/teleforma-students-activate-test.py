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
    help = "Activate all user account for subscribed students"
    username = 'test'
    
    def handle(self, *args, **options):
        period_name = args[-2]
        log_file = args[-1]
        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')
        users = User.objects.filter(username=self.username)
        period = Period.objects.get(name=period_name)

        for user in users:
            students = user.student.all()
            if students:
                student = students[0]
                if student.is_subscribed and not user.is_active and student.period == period:
                    user.is_active = True
                    user.save()
                    logger.logger.info('init : ' + user.username)

        logger.logger.info('############## Done #################')
