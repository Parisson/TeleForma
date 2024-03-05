from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import Organization, Department
import logging
import codecs


class Command(BaseCommand):
    help = "create a new department with organization, name and domain"
    admin_email = 'webmaster@parisson.com'
    args = 'organization_name name domain'

    def handle(self, *args, **options):
        organization_name = args[0]
        name = args[1]
        domain = args[2]

        organization = Organization.objects.get(name=organization_name)
        department, c = Department.objects.get_or_create(
            organization=organization,
            name=name,
            domain=domain
            )
        department.save()

