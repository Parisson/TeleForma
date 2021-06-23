from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *


class Command(BaseCommand):
    help = "Unpublish all contents for a given period"
    args = "period_name"
    admin_email = 'webmaster@parisson.com'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        period_name = args[0]
        period = Period.objects.get(name=period_name)
        conferences = Conference.objects.filter(period=period)
        for conference in conferences:
            conference.status = 0
            conference.save()
            for media in conference.media.all():
                media.is_published = False
                media.save()
        # <HACK
        for document in Document.objects.all():
            if document.file:
                document.is_published = True
                document.save()
        # HACK>

        for document in period.document.all():
            document.is_published = False
            document.save()

        