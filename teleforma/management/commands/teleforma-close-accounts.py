from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from teleforma.models import *
import datetime

class Command(BaseCommand):
    help = "Close account of students tied to expired periods"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        today = datetime.date.today()
        for period in Period.objects.filter(date_close_accounts__lte = today):
            for student in period.student.filter(user__is_active = True):
                print "Closing %s %s" % (student, student.user_id)
                student.restricted = True
                student.save()
