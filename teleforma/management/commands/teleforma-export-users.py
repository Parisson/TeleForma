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
from xlwt import Workbook

class Command(BaseCommand):
    help = "Export users to a XLS file (see an example in example/data/"
    args = "path"
    first_row = 2
    admin_email = 'webmaster@parisson.com'

    def export_user(self, count, user):
        student = Student.objects.filter(user=user)
        if student:
            student = Student.objects.get(user=user)
            row = self.sheet.row(count)
            row.write(0, user.last_name)
            row.write(1, user.first_name)
            row.write(9, user.email)

            row.write(2, unicode(student.iej))
            row.write(3, unicode(student.training))
            row.write(4, unicode(student.procedure))
            row.write(5, unicode(student.written_speciality))
            row.write(6, unicode(student.oral_speciality))
            row.write(7, unicode(student.oral_1))
            row.write(8, unicode(student.oral_2))
            row.write(15, unicode(student.category))
#            address     = row[10].value
#            p_code      = row[11].value
#            city        = row[12].value
#            tel         = row[13].value
#            date        = row[14].value

            print 'exported: ' + user.first_name + ' ' + user.last_name + ' ' + user.username



    def handle(self, *args, **options):
        file = args[0]
        self.book = Workbook()
        self.sheet = self.book.add_sheet('Etudiants')
        users = User.objects.all()
        count = 0
        for user in users:
            self.export_user(count, user)
            count += 1
        self.book.save(file)


