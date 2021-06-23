from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.exam.models import *
import logging
import codecs


class Command(BaseCommand):
    help = "Print quota levels"

    def handle(self, *args, **options):
        qs=Quota.objects.all()
        for q in qs:
            print q.corrector, q.level

