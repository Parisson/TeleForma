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
                    print ("seminar cloning:", seminar)
                    seminar.period = from_period
                    seminar.save()
                    clone = seminar.clone()
                    clone.publish_date = seminar.publish_date.replace(year=to_year)
                    clone.expiry_date = seminar.expiry_date.replace(year=to_year)
                    clone.period = to_period 
                    clone.save()
                    print ('seminar dates updated', clone)

                    for field in seminar._meta.many_to_many:
                        if field.rel.to == Document:
                            source = getattr(seminar, field.attname)
                            destination = getattr(clone, field.attname)

                            for item in source.all():
                                item.period = from_period
                                item.save()
                                item_clone = item.clone()
                                item_clone.readers = []
                                item_clone.period = to_period
                                item_clone.save()
                                destination.remove(item)
                                destination.add(item_clone)
                                print ("media cloned and assigned:", item_clone)

                    for question in seminar.question.all():
                        question_clone = question.clone()
                        question_clone.seminar = clone
                        question_clone.save()
                        print ("question cloned and assigned:", question_clone)
                
                else:
                    seminar.period = to_period
                    seminar.save()


