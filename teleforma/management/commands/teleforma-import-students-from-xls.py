from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.views import UserXLSBook
import logging
import json


class Command(BaseCommand):
    help = "Import Students from XLS file"
    args = "path"
    admin_email = 'webmaster@parisson.com'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        file = args[0]
        period = args[1]
        xls = UserXLSBook()
        xls.read(file, period)



