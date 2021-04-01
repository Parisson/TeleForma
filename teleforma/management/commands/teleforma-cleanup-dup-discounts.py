from django.core.management.base import BaseCommand
from teleforma.models import *

class Command(BaseCommand):
    help = "Cleanup duplicate discount objects"

    def handle(self, *args, **options):
        for student in Student.objects.all():
            known = set()
            for discount in student.discounts.all():
                key = (discount.value, discount.description)
                if key in known:
                    print("Deleting %d (%s: %s)" % (discount.id, student, key))
                    discount.delete()
                else:
                    known.add(key)

