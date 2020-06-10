# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from teleforma.webclass.models import *
from teleforma.models import *

from postman.utils import email_visitor, notify_user
from postman.models import Message

WARN_DELAY_MAX = 15
WARN_DELAY_MIN = 5

class Command(BaseCommand):
    help = "Send the Webclass will start notifications"

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        dow = now.weekday()
        begin = now + datetime.timedelta(minutes=WARN_DELAY_MIN)
        end = now + datetime.timedelta(minutes=WARN_DELAY_MAX)
        slots = WebclassSlot.objects.filter(day = dow,
                                            start_hour__gte = begin.time(),
                                            start_hour__lt = end.time())
        site = Site.objects.all()[0]
        admin = User.objects.get(username = 'Admin-CRFPA')
        date = now.strftime('%d/%m/%Y')
        for slot in slots:
            hour = slot.start_hour.strftime('%Hh%M')
            print("Sending notifications for %s:%s (%s)" % (slot.webclass.course,
                                                            slot.start_hour,
                                                            slot.id))
            subject = "Webclass_%s_%s_%s" % (slot.webclass.course,
                                             date, hour)
                                             
            body = """Votre Webclasse va commencer."""

            users = slot.participants.all()
            for user in users:
                print(" => %s" % user)
                msg = Message(subject = subject,
                              body = body,
                              sender = admin,
                              recipient = user)
                msg.moderation_status = 'a'
                msg.save()
                notify_user(msg, 'acceptance', site)                          

