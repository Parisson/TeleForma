from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import codecs
import xlrd
import datetime

class Command(BaseCommand):
    help = "Import users from a XLS file (see an example in example/data/"
    args = "path period_name"
    first_row = 2
    admin_email = 'webmaster@parisson.com'
    DEBUG = True

    def get_courses(self, code):
        courses = Course.objects.filter(code=code)
        if courses:
            return courses[0]
        else:
            return None

    def get_training(self, code):
        period, c = Period.objects.get_or_create(name=self.period_name)
        platform_only = False
        if 'I' in code[0:2]:
            platform_only = True
            code = code[4:]
            training, c = Training.objects.get_or_create(code=code, period=period)
        else:
            training, c = Training.objects.get_or_create(code=code, period=period)
        return platform_only, training

    def get_iej(self, name):
        iejs = IEJ.objects.filter(name=name)
        if iejs:
            iej = iejs[0]
        elif not name:
            iej = None
        else:
            iej, c = IEJ.objects.get_or_create(name=name)
        return iej

    def import_user(self, row, period_name):
        self.period_name = period_name
        last_name   = row[0].value
        first_name  = row[1].value
        email       = row[9].value

        if self.DEBUG:
            email       = self.admin_email

        username = slugify(first_name)[0] + '.' + slugify(last_name)
        username = username[:30]

        users = User.objects.filter(username=username)

        if users and self.DEBUG:
            for user in users:
                user.delete()

        i = 1
        while users:
            username = slugify(first_name)[:i] + '.' + slugify(last_name)
            username = username[:30]
            users = User.objects.filter(username=username)
            if not users:
                break
            i += 1

        date = row[14].value
        date_joined = datetime.datetime(*xlrd.xldate_as_tuple(date, self.book.datemode))

        user, created = User.objects.get_or_create(username=username, first_name=first_name,
                                     last_name=last_name, email=email, date_joined = date_joined)

        if created:
            student = Student.objects.filter(user=user)
            if student:
                student.delete()
            student = Student(user=user)
            student.platform_only, student.training = self.get_training(row[3].value)
            student.iej = self.get_iej(row[2].value)
            student.save()

            student.period = Period.objects.filter(name=self.period_name)
            student.procedure = self.get_courses(row[4].value)
            student.written_speciality = self.get_courses(row[5].value)
            student.oral_speciality = self.get_courses(row[6].value)
            student.oral_1 = self.get_courses(row[7].value)
            student.oral_2 = self.get_courses(row[8].value)

            profile, created = Profile.objects.get_or_create(user=user)
            profile.address = row[10].value
            profile.postal_code = row[11].value
            profile.city = row[12].value
            profile.telephone = row[13].value
            profile.save()
            student.save()
            print 'imported: ' + first_name + ' ' + last_name + ' ' + username

    def handle(self, *args, **options):
        file = args[0]
        period_name = args[1]
        self.book = xlrd.open_workbook(file)
        sheet = self.book.sheet_by_index(0)
        col = sheet.col(0)
        for i in range(self.first_row, len(col)):
            self.import_user(sheet.row(i), period_name)

