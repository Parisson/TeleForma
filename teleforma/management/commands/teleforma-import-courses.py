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

class Command(BaseCommand):
    help = "Import courses from a txt file (see an example in example/data/"
    args = "organization path"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        organization = args[0]
        path = args[1]
        file = open(path, 'r')
        department = os.path.splitext(os.path.basename(path))[0]
        organization, created = Organization.objects.get_or_create(name=organization)
        department, created = Department.objects.get_or_create(name=department,
                                                               organization=organization)
        types = CourseType.objects.all()

        for code in file.readlines():
            course, created = Course.objects.get_or_create(code=code, department=department,
                                                           title=code.replace('_', ' '))






