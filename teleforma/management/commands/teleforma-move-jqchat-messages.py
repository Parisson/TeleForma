from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from jqchat.models import *
import datetime


class Command(BaseCommand):
    help = "Move some jqchat messages from one room to another past to a given date"
    args = "from_room to_room year month day"

    def handle(self, *args, **options):
        day = args[-1]
        month = args[-2]
        year = args[-3]
        to_room_name = args[-4]
        from_room_name = args[-5]

        date = datetime.datetime(int(year), int(month), int(day))
        to_room = Room.objects.get(name=to_room_name)
        from_room = Room.objects.get(name=from_room_name)

        messages = Message.objects.filter(room=from_room, created__gte=date)
        for message in messages:
            message.room = to_room
            message.save()

