from django.core.management.base import BaseCommand
from teleforma.exam.models import Script
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Delete all exam scripts older than a number of days"

    def handle(self, *args, **options):
        days = args[0]
        date_limit = datetime.today() - timedelta(days=days)
        for script in Script.objects.filter(date_added__lte=date_limit):
            script.delete()
