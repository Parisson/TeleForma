from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import json
import datetime
import sys

class Command(BaseCommand):
    help = "Delete all conferences between two dates"
    args = "start_month start_year end_month end_year"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        period_name, start_month, start_year, end_month, end_year = args[-5], int(args[-4]), \
                                    int(args[-3]), int(args[-2]), int(args[-1])
        periods = Period.objects.filter(name=period_name)
        if not periods:
            sys.exit("No such period")
        else:
            period = periods[0]
        start_time = datetime.datetime(start_year, start_month, 1, 0, 0)
        end_time = datetime.datetime(end_year, end_month, 30, 23, 59)
        conferences = Conference.objects.filter(date_begin__gte=start_time, period=period)
        conferences = conferences.filter(date_begin__lte=end_time, period=period)
        for conference in conferences:
            medias = Media.objects.filter(conference=conference)
            for media in medias:
                media.delete()
            conference.delete()
        print str(len(conferences)) + ' conferences and related media deleted.'
