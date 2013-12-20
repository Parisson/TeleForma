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
from postman.models import *
from postman.utils import email_visitor, notify_user
from teleforma.context_processors import seminar_validated


class Command(BaseCommand):
    help = """Send a reminder to all users when their subscripted seminars 
            expire before a given number of days"""
    args = ['days',]
    message_template = 'teleforma/messages/seminar_remind.txt'
    subject_template = 'teleforma/messages/seminar_remind_subject.txt'
    language_code = 'fr_FR'

    def handle(self, *args, **kwargs):
        days = int(args[-1])
        users = User.objects.all()
        translation.activate(self.language_code)
        sender_email = settings.DEFAULT_FROM_EMAIL
        sender = User.objects.get(email=sender_email)
        today = datetime.datetime.now()

        for user in users:
            auditor = user.auditor.all()
            professor = user.professor.all()
            seminars = []

            if auditor and not professor and user.is_active and user.email:
                auditor = auditor[0]
                context = {}
                all_seminars = auditor.seminars.all()
                
                for seminar in all_seminars:
                    if seminar.expiry_date:
                        delta = seminar.expiry_date - today
                        if delta.days < days and not seminar_validated(user, seminar):
                            seminars.append(seminar)

                if seminars:
                    context['organization'] = seminars[0].course.department.name
                    context['gender'] = auditor.get_gender_display()
                    context['first_name'] = user.first_name
                    context['last_name'] = user.last_name
                    context['site'] = Site.objects.get_current()
                    context['seminars'] = seminars
        
                    text = render_to_string(self.message_template, context)
                    subject = render_to_string(self.subject_template, context)
                    # subject = '%s : %s' % (seminar.title, subject)

                    mess = Message(sender=sender, recipient=user, subject=subject[:119], body=text)
                    mess.moderation_status = 'a'
                    mess.save()
        
                    if not settings.DEBUG:
                        notify_user(mess, 'acceptance')
                    
