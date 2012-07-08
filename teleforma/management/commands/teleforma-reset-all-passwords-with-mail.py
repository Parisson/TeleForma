from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
from postman import *


class Command(BaseCommand):
    help = "Reset the password for all (active) users "
    message_template = 'postman/email_user_init.html'
    subject_template = 'postman/email_user_subject_init.html'

    def init_password_email(self, user):
        site = Site.objects.get_current()
        ctx_dict = {'site': site, 'organization': settings.TELEMETA_ORGANIZATION, 'usr': user}
        subject = render_to_string(subject_template, ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string(message_template, ctx_dict)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        profile = user.get_profile()
        profile.init_password = True
        profile.save()
        mail_admins(subject, message)

    def handle(self, *args, **options):
#        users = User.objects.all()
        users = User.objects.filter(is_staff=True)
        for user in users:
            profile = user.get_profile()
            if not profile.init_password and user.is_active:
                self.init_password_email(user)

