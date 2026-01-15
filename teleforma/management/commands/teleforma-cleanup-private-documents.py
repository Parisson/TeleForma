from django.core.management.base import BaseCommand
from teleforma.models import DocumentPrivate
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Delete all private documents older than a number of days"
    args = "days"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        days = int(args[0])
        date_limit = datetime.today() - timedelta(days=days)
        documents = DocumentPrivate.objects.filter(date_added__lte=date_limit)
        print("num of docs: ", documents.count())
        for document in documents:
            document.delete()
            print(document.id, "deleted")
