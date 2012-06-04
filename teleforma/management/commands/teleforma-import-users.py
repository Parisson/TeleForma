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

    def get_first_course(self, code):
        courses = Course.objects.filter(code__in=code)
        if courses:
            return [courses[0]]
        else:
            raise 'You should first create a course with this code:' + code

    def import_user(self, row):
        last_name   = row[0].value
        first_name  = row[1].value
        email       = row[9].value
        #FIXME:
        email       = self.admin_email
        username = slugify(first_name)[0] + '.' + slugify(last_name)
        username = username[:30]
        date = row[14].value
        date_joined = datetime.datetime(*xlrd.xldate_as_tuple(date, self.book.datemode))

        #FIXME: not for prod
        user = User.objects.filter(username=username)
        if user:
            user.delete()

        user, created = User.objects.get_or_create(username=username, first_name=first_name,
                                     last_name=last_name, email=email, date_joined = date_joined)

        if created:
            student = Student.objects.filter(user=user)
            if not student:
                student = Student(user=user)
                student.period, c = Period.objects.get_or_create(name='Estivale')
                student.iej, c = IEJ.objects.get_or_create(name=row[2].value)
                student.training, c = Training.objects.get_or_create(code=row[3].value)
                student.save()

            student.procedure = self.get_first_course(row[4].value)
            student.written_speciality = self.get_first_course(row[5].value)
            student.oral_speciality = self.get_first_course(row[6].value)
            student.oral_1 = self.get_first_course(row[7].value)
            student.oral_2 = self.get_first_course(row[8].value)

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




