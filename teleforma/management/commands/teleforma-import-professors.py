from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import json


class Command(BaseCommand):
    help = "Import professors from a JSON file"
    args = "path"
    admin_email = 'webmaster@parisson.com'


    def import_professors(self, data):
        professors = json.loads(data)
        for professor in professors:
            user, c = User.objects.get_or_create(username=professor['username'],
                                                 first_name=professor['first_name'],
                                                 last_name=professor['last_name'],
                                                 email=professor['email'])
            if c:
                p = Professor(user=user)
                p.save()
                for code in professor['courses']:
                    course = Course.objects.get(code=code)
                    p.courses.add(course)
                print 'imported: ' + user.first_name + ' ' + user.last_name + ' ' + user.username

    def handle(self, *args, **options):
        file = args[0]
        f = open(file, 'r')
        data = f.read()
        f.close()
        self.import_professors(data)




