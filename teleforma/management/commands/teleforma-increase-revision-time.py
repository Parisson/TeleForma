from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from django.utils import translation
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import datetime


class Command(BaseCommand):
    help = """Manually increase seminar revision time"""

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            auditor = user.auditor.all()
            professor = user.professor.all()
            if auditor and not professor and user.is_active and user.email:
                auditor = auditor[0]
                context = {}
                seminars = auditor.seminars.all()
                for seminar in seminars:
                    revisions = SeminarRevision.objects.filter(user=user, seminar=seminar)
                    if revisions:
                        if not revisions[0].date_modified and len(revisions) > 1:
                            revision = revisions[1]
                        else:
                            revision = revisions[0]
                        delta = datetime.timedelta(seconds=seminar.duration.as_seconds())
                        revision.date_modified = revision.date_modified + delta
                        revision.save()