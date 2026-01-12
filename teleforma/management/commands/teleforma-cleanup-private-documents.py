from django.core.management.base import BaseCommand
from teleforma.models import DocumentPrivate
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Delete all private documents older than a number of days"

    def handle(self, *args, **options):
        days = args[0]
        date_limit = datetime.today() - timedelta(days=days)
        for document in DocumentPrivate.objects.filter(date_added__lte=date_limit):
            document.delete()
