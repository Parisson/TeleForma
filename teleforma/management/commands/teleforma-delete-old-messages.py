from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
from postman.models import Message
import logging
import datetime


class Command(BaseCommand):
    help = "Delete postman messages olders than one year"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        date = datetime.datetime.now()
        date.year = date.year - 1
        print(date)
        messages = Message.objects.filter(sent_at__lte=datetime_now)
        print(messages.count())
        for message in messages:
            print(message.sent_at)
            message.delete()

