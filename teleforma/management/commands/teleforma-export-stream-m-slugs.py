from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *
import logging
import json

class Command(BaseCommand):
    help = "Export course slugs to a Stream-M server conf file"
    args = "password, path"
    admin_email = 'webmaster@parisson.com'
    ext = 'webm'
    data = """
# server.bindAddress
# example: 127.0.0.1, 192.168.1.1
# localhost. www.example.com also work
#server.bindAddress = 192.168.0.12

# server.port
# listening port
http.port=8080

streams.safe=true
streams.safe.password=source2parisson
streams.safe.limit=100
"""

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def export(self):
        courses = Course.objects.all()
        types = CourseType.objects.all()
        for course in courses:
            for type in types:
                slug = course.slug + '-' + slugify(type.name.lower())
                slug = slugify(course.department.name.lower()) + '-' + slug
                self.data += '\nstreams.' + slug + '=true\n'
                self.data += 'streams.' + slug + '.password=' + self.passwd + '\n'
                self.data += 'streams.' + slug + '.limit=1000\n'

    def handle(self, *args, **options):
        self.passwd = args[0]
        file = args[1]
        self.export()
        f = open(file, 'w')
        f.write(self.data)
        f.close()
