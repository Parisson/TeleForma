# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import os
import timeside


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
    help = "Copy conferences from one period to another"
    courses = ['OB','PAC','PC','PP','DA','Affaires','DIE','Civil','Penal','Social']
    period_1_name = u'Semestrielle'
    period_2_name = u'Pré-Estivale'

    def handle(self, *args, **options):
        period_1 = Period.objects.get(name=self.period_1_name)
        period_2 = Period.objects.get(name=self.period_2_name)
        for course_code in self.courses:
            course = Course.objects.get(code=course_code)
            medias = Media.objects.filter(period=period_1, course=course)
            for media in medias:
                media.pk = None
                media.save()
                media.period = period_2
                media.save()
