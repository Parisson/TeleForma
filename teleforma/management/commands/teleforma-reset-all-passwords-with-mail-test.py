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
    help = "Reset the password for all (active) users "
    message_template = 'postman/email_user_init.txt'
    subject_template = 'postman/email_user_subject_init.txt'
    language_code = 'fr_FR'
    username = 'test'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def init_password_email(self, user):
        site = Site.objects.get_current()
        ctx_dict = {'site': site, 'organization': settings.TELEFORMA_ORGANIZATION, 'usr': user}
        subject = render_to_string(self.subject_template, ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.message_template, ctx_dict)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

    def handle(self, *args, **options):
        log_file = args[-1]
        period_name = args[-2]
        logger = Logger(log_file)
        logger.logger.info('########### Processing #############')

        period = Period.objects.get(name=period_name)
        users = User.objects.filter(username=self.username)
        translation.activate(self.language_code)

        for user in users:
            profile, c = Profile.objects.get_or_create(user=user)
            students = user.student.all()
            if students:
                student = students[0]
            else:
                student = Student()
            professors = user.professor.all()
            quotas = user.quotas.all()
            if student.period == period or professors or quotas:
                if profile and user.is_active:
                    if not profile.init_password and user.email:
                        self.init_password_email(user)
                        profile.init_password = True
                        profile.save()
                        logger.logger.info('init : ' + user.username)

        logger.logger.info('############## Done #################')
