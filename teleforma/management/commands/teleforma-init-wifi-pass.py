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
import random, string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Command(BaseCommand):
    help = "init all user wifi pass"
    args = 'path'

    def handle(self, *args, **options):
        path = args[0]
        f = open(path, 'w')

        for user in User.objects.all():
            profile = user.profile.get()
            if not profile.wifi_pass:
                profile.wifi_login = user.username
                profile.wifi_pass = id_generator(8)
                profile.save()
                f.write(profile.wifi_login + ',' + profile.wifi_pass + '\n')

        f.close()
