from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.exam.models import *
import logging
import codecs


class Command(BaseCommand):
    help = "submit all script to Box View"

    def handle(self, *args, **options):
    	for script in Script.objects.all():
    		script.submit()
    		script.save()
