from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.exam.models import *
import logging
import codecs


class Command(BaseCommand):
    help = "Export all WiFi accounts"
    args = 'path'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        path = args[0]
        period_name = args[1]

        f = open(path, 'w')
        period = Period.objects.get(name=period_name)
        
        for user in User.objects.all():
            profile = Profile.objects.filter(user=user)
            students = user.student.all()
            if profile and students:
            	p = profile[0]
                student = students[0]
                if student.is_subscribed and user.is_active and student.period == period:
                    data = []
                    data.append(p.wifi_login)
                    data.append(p.wifi_pass)
                    data.append('\n')
                    s = ','.join(data)
                    f.write(s.encode('utf8'))
        f.close()

