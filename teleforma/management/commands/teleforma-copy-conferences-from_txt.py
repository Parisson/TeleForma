# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *
import logging
import os
from copy import deepcopy

class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Copy conferences from one period to another from a text file containing conf IDs"
    period_from_name = 'Estivale'
    period_to_name = 'Semestrielle'

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        path = args[0]
        txt_file = open(path, 'r')
        public_ids = txt_file.readlines()
        period_from = Period.objects.get(name=self.period_from_name)
        period_to = Period.objects.get(name=self.period_to_name)

        for public_id in public_ids:
            public_id = public_id.replace('\n', '').replace(' ', '')
            print(public_id)
            conference = Conference.objects.get(public_id=public_id)
            medias = deepcopy(conference.media.all())
            conference.pk = None
            conference.public_id = None
            conference.period = period_to
            conference.save()
            print(conference.public_id)
            for media in medias:
                media.pk = None
                media.save()
                media.period = period_to
                media.conference = conference
                media.save()
