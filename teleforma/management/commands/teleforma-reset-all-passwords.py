from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import codecs
import xlrd
from xlwt import Workbook

class Command(BaseCommand):
    help = "Reset the password for all (active) users with given E-Mail adress"
    admin_email = 'webmaster@parisson.com'
    from_email = 'webmaster@parisson.com'

    def reset_password_email(self, email, template='telemeta/registration/password_reset_email.html'):
        form = PasswordResetForm({'email': email})
        opts = {'from_email':self.from_email, 'email_template_name':template,
                         'token_generator': default_token_generator }
        return form.save(**opts)

    def handle(self, *args, **options):
#        users = User.objects.all()
        users = User.objects.filter(is_staff=True)
        for user in users:
            self.reset_password_email(user.email)

