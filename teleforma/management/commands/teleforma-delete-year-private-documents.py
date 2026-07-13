import os
import datetime
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import DocumentPrivate


class Command(BaseCommand):
    help = "Delete all private docs older than a given year"
    args = "year"
    admin_email = 'webmaster@parisson.com'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        year = int(args[0])
        date = datetime.datetime(day=31, month=12, year=year)
        docs = DocumentPrivate.objects.filter(date_added__lte=date)
        for doc in docs:
            doc.delete()
        