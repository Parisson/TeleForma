from django.core.management.base import BaseCommand
from teleforma.models import *

import datetime

class Command(BaseCommand):
    help = "Create missing schedule objects"

    def handle(self, *args, **options):
        threshold = datetime.date(2021, 2, 2)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        date1 = datetime.date(2021, 6, 30)
        date2 = datetime.date(2021, 7, 31)

        full = ((0.30, tomorrow),
                (0.35, date1),
                (0.35, date2))
        partial = ((0.5, date1),
                   (0.5, date2))
                
        for student in Student.objects.all():
            if not student.date_subscribed or not student.period:
                continue
            if student.period.name != 'Estivale':
                continue
            if student.date_subscribed.date() < threshold:
                continue
            if student.payment_type != 'online':
                continue
            student.update_balance()
            if student.balance_intermediary >= 0:
                continue            

            if len(student.payments.all()) > 0:
                schedule = partial
            else:
                schedule = full

            balance = student.balance_intermediary
            for ratio, date in schedule:
                amount = -balance * ratio
                p = Payment(student = student,
                            value = amount,
                            month = date.month,
                            scheduled = date)
                p.save()
                print("Student %d: created %d" % (student.id, p.id))
