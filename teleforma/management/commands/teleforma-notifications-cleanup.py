from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from teleforma.models.notification import Notification
from datetime import datetime

class Command(BaseCommand):
    help = "Cleanup notifications"
   
    def handle(self, *args, **options):
        Notification.objects.filter(expired__lt=datetime.now()).delete()
       
        