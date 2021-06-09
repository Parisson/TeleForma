from optparse import make_option
from teleforma.models.core import Conference
from teleforma.models.chat import ChatMessage
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Broadcast a chat message"
    args = "username text"

    def handle(self, *args, **options):
        # text = args[1]
        # username = args[0]
        ChatMessage.live_conference_message(Conference.objects.get(id=7815))


