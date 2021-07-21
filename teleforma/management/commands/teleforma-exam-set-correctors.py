from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.exam.models import *
import logging
import codecs


class Command(BaseCommand):
    help = "Set corrector to unassigned pending scripts"

    def handle(self, *args, **options):
        scripts = Script.objects.filter(corrector=None, status='3')
        for script in scripts:
            script.auto_set_corrector()
            print(f"set corrector {script.corrector} for script {script.id}")