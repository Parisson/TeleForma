from optparse import make_option
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import translation
from postman.models import Message

from teleforma.views.pro import get_seminar_delta
import datetime
from postman.utils import notify_user
from teleforma.context_processors import seminar_validated
import sys

class Command(BaseCommand):
    help = """Send a reminder to all users when their subscripted seminars 
            expire before a given number of days"""
    message_template = 'teleforma/messages/seminar_remind.txt'
    subject_template = 'teleforma/messages/seminar_remind_subject.txt'
    language_code = 'fr_FR'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int,
                            help='number of days')
        parser.add_argument('logfile', type=str, 
                            help='log file to use')

    def log(self, msg):
        today = datetime.datetime.now()
        print(today.strftime('%Y-%m-%d %H:%M'), msg)
        
    def handle(self, *args, **kwargs):
        days = kwargs['days']
        logpath = kwargs['logfile']
        sys.stdout = open(logpath, 'a', encoding='utf-8')

        self.log("Starting run")
        
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

                        completed = seminar_validated(user, seminar)
                        enough_time = get_seminar_delta(user, seminar)
                        validated = completed and enough_time > 0
                        if delta.days < days and delta.days >= 0 and not validated:
                            self.log("Seminar %s is about to expire" % seminar)
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
                    self.log("Sending mail to %s about %d seminars" % (user, len(seminars)))
                    
                    # mess = Message(sender=sender, recipient='yoanl@pilotsystems.net', subject=subject[:119], body=text)
                    mess.moderation_status = 'a'
                    mess.save()

                    if not settings.DEBUG:
                        site = Site.objects.all()[0]
                        notify_user(mess, 'acceptance', site)
                #
