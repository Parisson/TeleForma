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
    help = "Activate all user account for subscribed students"

    def handle(self, *args, **options):
        log_file = args[-1]
        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')
        users = User.objects.all()

        for user in users:
            student = user.student.all()
            if student:
                if student.is_subscribed and not user.is_active:
                    user.is_active = True
                    user.save()
                    logger.logger.info('init : ' + user.username)

        logger.logger.info('############## Done #################')
        
