# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *
import logging
import os
from copy import deepcopy
from teleforma.models.crfpa import Profile
from teleforma.forms import get_unique_username


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Copy students from one DB to another"
    period_name = 'Annuelle'
    db_from = 'recovery'
    db_to = 'default'
    logger = Logger('/var/log/app/student_import_recovery.log')

    def handle(self, *args, **options):
        period = Period.objects.get(name=self.period_name)

        students_from = Student.objects.using(self.db_from).filter(period=period)
        students_to = Student.objects.using(self.db_to).filter(period=period)

        user_tmp, c = User.objects.using(self.db_to).get_or_create(username='tmp')

        self.logger.logger.info('Number of student in from : ' + str(students_from.count()))
        self.logger.logger.info('Number of student in to : ' + str(students_to.count()))

        students_to_email = [student.user.email for student in students_to if (hasattr(student, 'user') and hasattr(student.user, 'email'))]

        new_students = []

        for student in students_from:
            # print(student)
            if student.trainings.all():
                if hasattr(student, 'user'):
                    if not student.user.email in students_to_email:
                        new_students.append(student)

        self.logger.logger.info('Number of new students to copy : ' + str(len(new_students)) + '\n')

        for student in new_students[100:]:
            user = deepcopy(student.user)
            payments = deepcopy(student.payments.all())
            discounts = deepcopy(student.discounts.all())
            optional_fees = deepcopy(student.optional_fees.all())
            paybacks = deepcopy(student.paybacks.all())
            trainings = student.trainings.all()
            profile = deepcopy(Profile.objects.using(self.db_from).get(user=student.user))

            user.pk = None
            user.username = get_unique_username(user.first_name, user.last_name)
            user.save(using=self.db_to)

            student.pk = None
            student.user = None
            student.save(using=self.db_to)
            student.user = user
            student.save(using=self.db_to)
            profile.pk = None
            profile.user = None
            profile.save(using=self.db_to)
            profile.user = user
            profile.save(using=self.db_to)

            for training in trainings:
                training_to = Training.objects.using(self.db_to).get(name=training.name, period=period)
                student.trainings.add(training_to)

            for payment in payments:
                payment.pk = None
                payment.save(using=self.db_to)
                payment.student = student
                payment.save(using=self.db_to)

            for discount in discounts:
                discount.pk = None
                discount.save(using=self.db_to)
                discount.student = student
                discount.save(using=self.db_to)

            for optional_fee in optional_fees:
                optional_fee.pk = None
                optional_fee.save(using=self.db_to)
                optional_fee.student = student
                optional_fee.save(using=self.db_to)

            for payback in paybacks:
                payback.pk = None
                payback.save(using=self.db_to)
                payback.student = student
                payback.save(using=self.db_to)

            self.logger.logger.info(str(student) + ' ' + student.user.username)

