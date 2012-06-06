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
    first_row = 1
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
            code = student.training.code
            if student.platform_only:
                code = 'I - ' + code
            row.write(3, unicode(code))
            row.write(4, unicode(student.procedure.code))
            row.write(5, unicode(student.written_speciality.code))
            row.write(6, unicode(student.oral_speciality.code))
            row.write(7, unicode(student.oral_1.code))
            row.write(8, unicode(student.oral_2.code))
            row.write(15, unicode(student.period))

            profile = Profile.objects.filter(user=user)
            if profile:
                profile = Profile.objects.get(user=user)
                row.write(10, profile.address)
                row.write(11, profile.postal_code)
                row.write(12, profile.city)
                row.write(13, profile.telephone)
                row.write(14, profile.date_added.strftime("%d/%m/%Y"))

            print 'exported: ' + user.first_name + ' ' + user.last_name + ' ' + user.username

    def export(self):
        self.book = Workbook()
        self.sheet = self.book.add_sheet('Etudiants')
        users = User.objects.all()
        row = self.sheet.row(0)
        row.write(0, 'NOM')
        row.write(1, 'PRENOM')
        row.write(2, 'IEJ')
        row.write(3, 'FORMATION')
        row.write(4, 'PROC')
        row.write(5, 'Ecrit Spe')
        row.write(6, unicode('Oral Spe'))
        row.write(7, 'ORAL 1')
        row.write(8, 'ORAL 2')
        row.write(9, 'MAIL')
        row.write(10, 'ADRESSE')
        row.write(11, 'CP')
        row.write(12, 'VILLE')
        row.write(13, 'TEL')
        row.write(14, "Date d'inscription")
        row.write(15, "Categorie")

        count = self.first_row
        for user in users:
            self.export_user(count, user)
            count += 1

        self.book.save(self.file)

    def handle(self, *args, **options):
        self.file = args[0]
        self.export()




