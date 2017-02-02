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
    help = "Copy courses from department to another"
    args = "organization department_from department_to"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        organization = args[0]
        department_from = args[1]
        department_to = args[1]
        organization, created = Organization.objects.get_or_create(name=organization)
        department_from, created = Department.objects.get_or_create(name=department_from, organization=organization)
        department_to, created = Department.objects.get_or_create(name=department_to, organization=organization)

        for course in department_from.course.all():
            course.pk = None
            course.department = department_to
            course.save()
