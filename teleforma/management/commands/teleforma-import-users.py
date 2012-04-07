from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
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

    def import_user(self, row):
        last_name = row[0].value
        first_name = row[1].value
        print first_name, last_name

    def handle(self, *args, **options):
        file = args[0]
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_index(0)
        col = sheet.col(0)
        for i in range(self.first_row, len(col)):
            self.import_user(sheet.row(i))

        print "Done, imported %s users" % str(i)



