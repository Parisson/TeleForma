from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.util.unaccent import unaccent
from teleforma.models import *
from teleforma.views import *
import logging
import codecs

class Command(BaseCommand):
    help = "pull teleforma conferences, periods and professors from a telecaster master servers"
    admin_email = 'webmaster@parisson.com'
    args = "Pre-Barreau"

    def handle(self, *args, **options):
        organization_name = args[-1]

        view = PeriodAccessMixin()
        view.pull(organization_name)

        view = CourseListView()
        view.pull(organization_name)

        view = ProfessorListView()
        view.pull()

