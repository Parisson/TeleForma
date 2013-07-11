from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from jqchat.models import *


class Command(BaseCommand):
    help = "Braodcast a jqchat message on the main site room by the admin"
    args = "text username"

    def handle(self, *args, **options):
        text = args[1]
        username = args[0]
        user = User.objects.get(username=username)
        room = Room.objects.get(name='site')
        message = Message.objects.create_message(user, room, text)

