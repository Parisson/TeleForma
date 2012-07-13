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
    help = "Export professors to a JSON file"
    args = "path"
    admin_email = 'webmaster@parisson.com'

    def export(self):
        list = []
        professors = Professor.objects.all()
        for professor in professors:
            user = professor.user
            courses = [course.code for course in professor.courses.all()]
            list.append({'username': user.username,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email,
                         'courses': courses,
                         })
            print 'exported: ' + user.first_name + ' ' + user.last_name + ' ' + user.username
        return json.dumps(list)


    def handle(self, *args, **options):
        file = args[0]
        json = self.export()
        f = open(file, 'w')
        f.write(json)
        f.close()




