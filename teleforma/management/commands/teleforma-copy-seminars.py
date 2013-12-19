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
        to_period, c = Period.objects.get_or_create(name=str(to_year))
        from_period, c = Period.objects.get_or_create(name=str(from_year))

        for seminar in Seminar.objects.all():
            if seminar.expiry_date:
                if seminar.expiry_date.year == from_year:
                    print ("cloning:", seminar)
                    clone = seminar.clone()
                    clone.publish_date = clone.publish_date.replace(year=to_year)
                    clone.expiry_date = clone.expiry_date.replace(year=to_year)
                    clone.save()
                    print ('dates updated', clone)

                    for field in seminar._meta.many_to_many:
                        if type(field.rel.to) == Document or type(field.rel.to) == Media:
                            source = getattr(seminar, field.attname)
                            destination = getattr(clone, field.attname)
                            for item in source.all():
                                print item
                                item.period = from_period
                                item.save()
                                item_clone = item.clone()
                                item_clone.readers = []
                                item_clone.period = to_period
                                item_clone.save()
                                destination.remove(item)
                                destination.add(item_clone)
                                print ("cloned and assigned:", item_clone)

                    questions = seminar.question.all()
                    for question in questions:
                        question_clone = question.clone()
                        question_clone.seminar = clone
                        question.save()
                        print ("cloned and assigned:", question)
