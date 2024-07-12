import os
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.exam.models import Script


class Command(BaseCommand):
    help = "Delete all exam scripts for a given period"
    args = "period_name"
    admin_email = 'webmaster@parisson.com'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        period_name = args[0]
        period = Period.objects.get(name=period_name)
        scripts = Script.objects.filter(period=period)
        for script in scripts:
            os.remove(script.file.path)
            script.delete()
        