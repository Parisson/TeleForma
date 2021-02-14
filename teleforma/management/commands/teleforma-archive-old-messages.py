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
    help = "Archive postman messages olders than one year"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        date_now = datetime.datetime.now()
        date_old = date_now.replace(year=date_now.year-1)
        print(date_old)
        messages = Message.objects.filter(sent_at__lte=date_old)
        print(messages.count())
        for message in messages:
            message.sender_archived = True
            message.recipient_archived = True
            message.save()

