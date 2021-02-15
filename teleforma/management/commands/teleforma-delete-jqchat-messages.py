
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from jqchat.models import Message
import datetime


class Command(BaseCommand):
    help = "Delete jqchat messages older than 1 year"

    def handle(self, *args, **options):
        date_now = datetime.datetime.now()
        date_old = date_now.replace(year=date_now.year-1)
        print(date_old)
        messages = Message.objects.filter(created__lte=date_old)
        print(messages.count())
        for message in messages:
            message.delete()
