from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.util.unaccent import unaccent
from teleforma.views import *
import logging
import json


class Command(BaseCommand):
    help = "Import Students from XLS file"
    args = "path"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        file = args[0]
        xls = UserXLSBook()
        xls.read(file)



