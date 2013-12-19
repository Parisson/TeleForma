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
import datetime


class Command(BaseCommand):
    help = """Copy some seminars and their content thanks to their expiry date year"""
    args = ['from_year to_year']
    language_code = 'fr_FR'

    def handle(self, *args, **kwargs):
        to_year = int(args[-1])
        from_year = int(args[-2])

        for seminar in Seminar.objects.all():
            if seminar.expiry_date.year == from_year:
                questions = seminar.question.all()
                seminar.pk = None
                seminar.save()
                seminar.publish_date.replace(year=from_year)
                seminar.expiry_date.replace(year=to_year)
                seminar.save()
                print ("updated:", seminar)

                for question in questions:
                    question.pk = None
                    question.save()
                    question.seminar = seminar
                    question.save()
                    print ("updated:", question)
