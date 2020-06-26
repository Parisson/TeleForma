from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
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

    def import_user(self, row, period_name):
        self.period_name = period_name
        last_name   = row[0].value
        first_name  = row[1].value
        email       = row[9].value

        user = User.objects.filter(first_name=first_name,
                                     last_name=last_name, email=email)

        if user:
            user = user[0]
            print 'update: ' + first_name + ' ' + last_name + ' ' + user.username
            student = user.student.get()
            student.oral_speciality = self.get_courses(row[6].value)
            student.oral_1 = self.get_courses(row[7].value)
            student.oral_2 = self.get_courses(row[8].value)
            student.save()

    def handle(self, *args, **options):
        file = args[0]
        period_name = args[1]
        self.book = xlrd.open_workbook(file)
        sheet = self.book.sheet_by_index(0)
        col = sheet.col(0)
        for i in range(self.first_row, len(col)):
            self.import_user(sheet.row(i), period_name)

