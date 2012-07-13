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
    args = "path"
    first_row = 2
    admin_email = 'webmaster@parisson.com'

    def get_courses(self, code):
        courses = Course.objects.filter(code=code)
        if courses:
            return courses[0]
        else:
            return None

    def get_training(self, code):
        platform_only = False
        if 'I' in code[0:2]:
            platform_only = True
            code = code[4:]
            training = Training.objects.get(code=code)
        else:
            training = Training.objects.get(code=code)
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

    def import_user(self, row):
        last_name   = row[0].value
        first_name  = row[1].value
        email       = row[9].value
        #FIXME: NOT for production
        email       = self.admin_email
        username = slugify(first_name)[0] + '.' + slugify(last_name)
        username = username[:30]
        date = row[14].value
        date_joined = datetime.datetime(*xlrd.xldate_as_tuple(date, self.book.datemode))

        #FIXME: NOT for production
        user = User.objects.filter(username=username)
        if user:
            user.delete()

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

            student.period = Period.objects.filter(name='Estivale')
            student.procedure = self.get_courses(row[4].value)
            student.written_speciality = self.get_courses(row[5].value)
            student.oral_speciality = self.get_courses(row[6].value)
            student.oral_1 = self.get_courses(row[7].value)
            student.oral_2 = self.get_courses(row[8].value)

            profile, created = Profile.objects.get_or_create(user=user)
            profile.address = row[10].value
            profile.postal_code = int(row[11].value)
            profile.city = row[12].value
            profile.telephone = row[13].value
            profile.save()
            student.save()
            print 'imported: ' + first_name + ' ' + last_name + ' ' + username

    def handle(self, *args, **options):
        file = args[0]
        self.book = xlrd.open_workbook(file)
        sheet = self.book.sheet_by_index(0)
        col = sheet.col(0)
        for i in range(self.first_row, len(col)):
            self.import_user(sheet.row(i))

