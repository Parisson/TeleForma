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

from postman.models import *
from postman.utils import email_visitor, notify_user



class Command(BaseCommand):
    help = "Broadcast a message to all users thanks to their subscription"
    message_template = 'teleforma/messages/seminar_remind.txt'
    subject_template = 'teleforma/messages/seminar_remind_subject.txt'
    language_code = 'fr_FR'

    def handle(self, *args, **options):
        users = User.objects.all()
        translation.activate(self.language_code)
        sender_email = settings.DEFAULT_FROM_EMAIL
        sender = User.objects.get(email=sender_email)

        for user in users:
            profile, c = Profile.objects.get_or_create(user=user)
            auditor = user.auditor.all()
            if auditor and profile and user.is_active and user.email:
                seminars = auditor.seminars.all()
                    for seminar in seminars:

                        organization = seminar.course.department.name
                        site = Site.objects.get_current()
                        path = reverse('teleforma-seminar-detail', kwargs={'pk':seminar.id})
                        gender = auditor[0].get_gender_display()

                        if seminar.sub_title:
                            title = seminar.sub_title + ' : ' + seminar.title
                        else:
                        
                        context['gender'] = gender
                        context['first_name'] = user.first_name
                        context['last_name'] = user.last_name
                        context['rank'] = answer.question.rank
                        context['site'] = site
                        context['path'] = path
                        context['title'] = title
                        context['organization'] = organization
                        context['date'] = seminar.expiry_date
                        
                        text = render_to_string(self.message_template, context)
                        subject = render_to_string(self.subject_template, context)
                        subject = '%s : %s' % (seminar.title, subject)

                        mess = Message(sender=sender, recipient=user, subject=subject[:119], body=text)
                        mess.moderation_status = 'a'
                        #mess.save()
                        #notify_user(mess, 'acceptance')
                        
                        print user.username, seminar.title

