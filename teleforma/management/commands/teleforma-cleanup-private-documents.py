from django.core.management.base import BaseCommand
from teleforma.models import *


class Command(BaseCommand):
    help = "Delete all private documents"

    def handle(self, *args, **options):
        for document in Document.objects.all():
            Document.delete()
