from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.exam.models import *
from teleforma.models.core import *
from teleforma.models.crfpa import *

import logging
import codecs
import random, string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Command(BaseCommand):
    help = "init all user wifi pass"

    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                profile = user.profile.get()
                if not profile.wifi_pass:
                    profile.wifi_login = user.username
                    profile.wifi_pass = id_generator(8)
                    profile.save()
            except:
                continue
