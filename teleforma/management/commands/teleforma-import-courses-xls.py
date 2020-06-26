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
    help = "Import courses from a XLS file (see an example in example/data/"
    args = "organization path"
    first_row = 2
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        organization = args[0]
        path = args[1]
        self.book = xlrd.open_workbook(path)
        sheet = self.book.sheet_by_index(0)
        col = sheet.col(0)

        department = os.path.splitext(os.path.basename(path))[0]
        organization, created = Organization.objects.get_or_create(name=organization)
        department, created = Department.objects.get_or_create(name=department,
                                                               organization=organization)

        for i in range(self.first_row, len(col)):
            course, c = Course.objects.get_or_create(title=sheet.row(i)[0].value,
                                                               code=sheet.row(i)[1].value,
                                                               number=int(sheet.row(i)[2].value),
                                                               department=department,)
            course.tweeter_title = sheet.row(i)[3].value
            course.save()

            if c:
                print 'imported: ' + course.title

