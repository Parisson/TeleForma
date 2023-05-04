from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from teleforma.models.notification import Notification




class Command(BaseCommand):
    help = "Notify user"
   

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('message', type=str)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        user_id = options['user_id']
        message = options['message']
        url = options['url']

        print(options)

        user = User.objects.get(pk=user_id)
        notif = Notification(message=message, user=user, url=url)
        notif.save()
        