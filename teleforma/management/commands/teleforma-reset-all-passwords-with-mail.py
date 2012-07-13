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


class Command(BaseCommand):
    help = "Reset the password for all (active) users "
    message_template = 'postman/email_user_init.txt'
    subject_template = 'postman/email_user_subject_init.txt'
    language_code = 'fr_FR'

    def init_password_email(self, user):
        site = Site.objects.get_current()
        ctx_dict = {'site': site, 'organization': settings.TELEMETA_ORGANIZATION, 'usr': user}
        subject = render_to_string(self.subject_template, ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.message_template, ctx_dict)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

    def handle(self, *args, **options):
        users = User.objects.all()
        translation.activate(self.language_code)
        for user in users:
            profile, c = Profile.objects.get_or_create(user=user)
            student = user.student.all()
            professor = user.professor.all()
            if student or professor:
                if profile and user.is_active:
                    if not profile.init_password and user.email:
                        self.init_password_email(user)
                        profile.init_password = True
                        profile.save()
                        print user.username

