from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from teleforma.models import *

class Command(BaseCommand):
    help = "Update the balance field on all users"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        for student in Student.objects.all():
            student.update_balance()
            print student, student.balance
