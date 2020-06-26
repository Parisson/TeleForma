from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *


class Command(BaseCommand):
    help = "Delete all conferences fir a given period"
    args = "period_name"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        period_name = args[0]
        period = Period.objects.get(name=period_name)
        conferences = Conference.objects.filter(period=period)
        for conference in conferences:
            print conference.public_id
            conference.delete()
        