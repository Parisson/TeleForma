
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import translation
from django.conf import settings
from teleforma.exam.models import *


class Command(BaseCommand):
    help = "Send a message"

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        sender = User.objects.filter(is_superuser=True)[0]
        site = Site.objects.all()[0]
        subject = 'Erreur dans la transmission de votre copie'
        scripts = Script.objects.filter(file='scripts/2014/07/22/home')
        print(scripts.count())

        for script in scripts:
            script.reject()
            context = {'script': script, 'site': site}
            text = render_to_string('exam/messages/script_fix.txt', context)
            print(text)
            mess = Message(sender=sender, recipient=script.author, subject=subject[:119], body=text)
            mess.moderation_status = 'a'
            mess.save()
            notify_user(mess, 'acceptance', site)

