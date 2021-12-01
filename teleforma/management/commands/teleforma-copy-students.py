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
import datetime


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
    periods_name = ['Estivale', 'Semestrielle']
    db_from = 'recovery'
    db_to = 'default'
    logger = Logger('/var/log/app/student_update_from_recovery-' + str(datetime.datetime.now) + '.log')
    date_limit_end = datetime.date(year=2021, month=8, day=6)
    date_limit_start = datetime.date(year=2021, month=8, day=1)

    def process_student(self, student, new=True):
            self.logger.logger.info('----------------------------------------------------------------')
            self.logger.logger.info('START of processing: ' + str(student) + ' ' + student.user.username + ' ' + student.user.email)

            user = deepcopy(student.user)
            payments = deepcopy(student.payments.all())
            discounts = deepcopy(student.discounts.all())
            optional_fees = deepcopy(student.optional_fees.all())
            paybacks = deepcopy(student.paybacks.all())
            trainings = student.trainings.all()
            profile = deepcopy(Profile.objects.using(self.db_from).get(user=student.user))

            if new:
                user.pk = None
                user.username = get_unique_username(user.first_name, user.last_name)
                user.save(using=self.db_to)
                self.logger.logger.info('user created: ' + user.username)

                student.pk = None
                student.user = None
                student.save(using=self.db_to)
                student.user = user
                student.save(using=self.db_to)
                self.logger.logger.info('student created: ' + student.user.username)

                profile.pk = None
                profile.user = None
                profile.save(using=self.db_to)
                profile.user = user
                profile.save(using=self.db_to)
                self.logger.logger.info('profile created: ' + profile.user.username)

                for training in trainings:
                    training_to = Training.objects.using(self.db_to).get(name=training.name, period=self.period)
                    student.trainings.add(training_to)
                    self.logger.logger.info('training added: ' + ' ' + student.user.username)
            else:
                students_to = Student.objects.using(self.db_to).filter(user__email=student.user.email, period=self.period)
                if students_to.count() > 1:
                    for s in students_to[1:]:
                        s.delete()
                        self.logger.logger.info('duplicated student deleted: ' + s.user.username)
                student_to = students_to[0]
                if student_to.is_subscribed != student.is_subscribed:
                    student_to.is_subscribed = student.is_subscribed
                    student_to.save()
                student = student_to
                #print(student)

            for payment in payments:
                date_created = deepcopy(payment.date_modified)
                date_paid = deepcopy(payment.date_paid)
                month = deepcopy(payment.month)
                scheduled = deepcopy(payment.scheduled)
                payments_to = Payment.objects.using(self.db_to).filter(student=student, month=month, scheduled=scheduled)
                if date_paid:
                    if payments_to:
                        payment_to = payments_to[0]
                        if date_paid != payment_to.date_paid and date_paid >= self.date_limit_start and date_paid <= self.date_limit_end:
                            payment_to.online_paid = payment.online_paid
                            payment_to.date_paid = payment.date_paid
                            payment_to.save()
                            self.logger.logger.info('payment updated: ' + student.user.username + \
                                     ', mois:' + str(month) + \
                                     ', date de création:' + str(date_created) + \
                                     ', date échéance:' + str(scheduled) + \
                                     ', date paid:' + str(date_paid) + \
                                     ', value: ' + str(payment.value))

            if new:
                for discount in discounts:
                    discount.pk = None
                    discount.save(using=self.db_to)
                    discount.student = student
                    discount.save(using=self.db_to)
                    self.logger.logger.info('discount added: ' + str(discount.value))

            optional_fees_to = student.optional_fees.all()
            for optional_fee_to in optional_fees_to:
                optional_fee_to.delete()
 
            for optional_fee in optional_fees:
                optional_fee.pk = None
                optional_fee.save(using=self.db_to)
                optional_fee.student = student
                optional_fee.save(using=self.db_to)
                self.logger.logger.info('optional_fee added: ' + str(optional_fee.value))

            paybacks_to = student.paybacks.all()
            for payback_to in paybacks_to:
                payback_to.delete()

            for payback in paybacks:
                payback.pk = None
                payback.save(using=self.db_to)
                payback.student = student
                payback.save(using=self.db_to)
                self.logger.logger.info('payback added: ' + str(payback.value))

            self.logger.logger.info('END of processing: ' + str(student) + ' ' + student.user.username)

    def handle(self, *args, **options):
        for period_name in self.periods_name:

            self.period = Period.objects.get(name=period_name)
            self.logger.logger.info('================================================================')
            self.logger.logger.info('PERIOD: ' + period_name)

            students_from = Student.objects.using(self.db_from).filter(period=self.period)
            students_to = Student.objects.using(self.db_to).filter(period=self.period)

            user_tmp, c = User.objects.using(self.db_to).get_or_create(username='tmp')

            self.logger.logger.info('Number of student in from : ' + str(students_from.count()))
            self.logger.logger.info('Number of student in to : ' + str(students_to.count()))

            students_to_email = []
            for student in students_to:
                try:
                    if hasattr(student, 'user'):
                        if student.user.email:
                            students_to_email.append(student.user.email)
                except:
                    continue

            new_students = []
            existing_students = []

            for student in students_from:
                # print(student)
                if student.trainings.all():
                    if hasattr(student, 'user'):
                        if not student.user.email in students_to_email:
                            new_students.append(student)
                        else:
                            existing_students.append(student)

            # print('new_students: ', len(new_students))
            # print('existing_students: ', len(existing_students))

            self.logger.logger.info('Number of new students to copy : ' + str(len(new_students)) + '\n')
            self.logger.logger.info('Number of new students to update : ' + str(len(existing_students)) + '\n')

            # for student in new_students:
            #     self.process_student(student)

            for student in existing_students:
                self.process_student(student, new=False)


