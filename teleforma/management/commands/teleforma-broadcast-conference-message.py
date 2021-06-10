from optparse import make_option
from teleforma.models.core import Conference
from teleforma.models.chat import ChatMessage
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Broadcast a chat conference message"

    def add_arguments(self, parser):
        parser.add_argument('conference_id', type=int)

    def handle(self, *args, **options):
        ChatMessage.live_conference_message(Conference.objects.get(id=options['conference_id']))


