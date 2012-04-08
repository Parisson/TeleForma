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

class Command(BaseCommand):
    help = "Import users from a XLS file (see an example in example/data/"
    args = "path"
    first_row = 2
    admin_email = 'webmaster@parisson.com'

    def import_user(self, row):
        last_name   = row[0].value
        first_name  = row[1].value
        email       = row[9].value
        #FIXME:
        email       = self.admin_email
        username = slugify(first_name)[0] + '.' + slugify(last_name)

        #FIXME: not for prod
        user = User.objects.get(username=username)
        user.delete()

        user, created = User.objects.get_or_create(username=username, first_name=first_name,
                                     last_name=last_name, email=email)


        if created:
            student = Student.objects.filter(user=user)
            if not student:
                student = Student(user=user)
            student.iej, c = IEJ.objects.get_or_create(name=row[2].value)
            student.training, c = Training.objects.get_or_create(code=row[3].value)
            student.procedure, c = Procedure.objects.get_or_create(code=row[4].value)
            student.written_speciality, c = Speciality.objects.get_or_create(code=row[5].value)
            student.oral_speciality, c = Speciality.objects.get_or_create(code=row[6].value)
            student.oral_1, c = Oral.objects.get_or_create(code=row[7].value)
            student.oral_2, c = Oral.objects.get_or_create(code=row[8].value)
            student.category, c = Category.objects.get_or_create(name=row[15].value)
            address     = row[10].value
            p_code      = row[11].value
            city        = row[12].value
            tel         = row[13].value
            date        = row[14].value

            student.save()
            print 'imported: ' + first_name + ' ' + last_name + ' ' + username



    def handle(self, *args, **options):
        file = args[0]
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_index(0)
        col = sheet.col(0)
        for i in range(self.first_row, len(col)):
            self.import_user(sheet.row(i))




