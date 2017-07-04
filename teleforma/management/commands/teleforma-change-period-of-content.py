from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *


class Command(BaseCommand):
    help = "Update period content of a year"
    args = "period_id_from period_id_to year"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        period_from_id = args[0]
        period_to_id = args[1]
        year = args[2]
        period_from = Period.objects.get(id=period_from_id)
        period_to = Period.objects.get(id=period_to_id)

        qss = []
        qss.append(Conference.objects.filter(period=period_from, date_added__year=year))
        qss.append(Document.objects.filter(period=period_from, date_added__year=year))
        qss.appedn(DocumentSimple.objects.filter(period=period_from, date_added__year=year))
        qqss.append(Media.objects.filter(period=period_from, date_added__year=year))

        for qs in qss:
            for obj in qs:
                obj.period = period_to
                obj.save()
