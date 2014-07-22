
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.exam.models import *
import logging
import codecs
import time, os


class Command(BaseCommand):
    help = "Send a message"

    def handle(self, *args, **options):
        sender = User.objects.filter(is_superuser=True)[0]
        site = Site.objects.all()[0]
        subject = 'Erreur dans la transmission de votre copie'
        scripts = Script.objects.filter(file='scripts/2014/07/22/home')
        print scripts.count()

        for script in scripts:
            context = {'script': self, 'site': site}
            text = render_to_string('exam/messages/script_fix.txt', context)
            print text
            mess = Message(sender=sender, recipient=script.author, subject=subject[:119], body=text)
            mess.moderation_status = 'a'
            #mess.save()
            #notify_user(mess, 'acceptance', site)

