from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *
from teleforma.exam.models import *


class Command(BaseCommand):
    help = "Update period content of a year"
    args = "period_id_from period_id_to year"
    admin_email = 'webmaster@parisson.com'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        period_from_id = args[0]
        period_to_id = args[1]
        year = args[2]
        period_from = Period.objects.get(id=period_from_id)
        period_to = Period.objects.get(id=period_to_id)

        qss = []
        qss.append(Conference.objects.filter(period=period_from, date_begin__year=year))
        qss.append(Document.objects.filter(period=period_from, date_added__year=year))
        qss.append(DocumentSimple.objects.filter(period=period_from, date_added__year=year))
        qss.append(Media.objects.filter(period=period_from, date_added__year=year))

        for qs in qss:
            for obj in qs:
                obj.period = period_to
                obj.save()

        for obj in Script.objects.filter(period=period_from, date_added__year=year):
            obj.period = period_to
            obj.update()
