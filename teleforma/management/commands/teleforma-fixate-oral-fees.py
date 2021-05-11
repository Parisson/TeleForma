from django.core.management.base import BaseCommand
from teleforma.models import *

import datetime

class Command(BaseCommand):
    help = "Create missing schedule objects"

    def handle(self, *args, **options):
        date = datetime.date(2021, 8, 31)
        amount = 250
        
        for student in Student.objects.all():
            if not student.date_subscribed or not student.period or not student.oral_1:
                continue
            if student.period.name != 'Estivale':
                continue
            if student.payment_type != 'online':
                continue
            if student.oral_1.title != 'Anglais':
                continue

            found = False
            for fee in student.optional_fees.all():
                if fee.value == amount:
                    found = True
            if found:
                continue
            p = Payment(student = student,
                        value = amount,
                        month = date.month,
                        scheduled = date)
            p.save()
            f = OptionalFee(student = student,
                            value = amount,
                            description = "Option langue")
            f.save()
            print("Student %d: created %d / %d" % (student.id, p.id, f.id))
