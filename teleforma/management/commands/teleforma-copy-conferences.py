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
    help = "Copy conferences from one period to another"
    # courses = ['OB','PAC','PC','PP','DA','Civil','Fiscal','Affaires','DIE','Penal','Social']
    course_codes = ['Libertes',]
    period_from_name = 'Estivale'
    period_to_name = 'Semestrielle'
    course_types = ['Cours', 'Corrections', 'Capsules']

    def handle(self, *args, **options):
        period_from = Period.objects.get(name=self.period_from_name)
        period_to = Period.objects.get(name=self.period_to_name)

        for course_code in self.course_codes:
            course = Course.objects.get(code=course_code)
            for course_type in self.course_types:
                course_type = CourseType.objects.get(name=course_type)
                medias = Media.objects.filter(course=course, course_type=course_type, is_published=True)
                conferences = course.conference.filter(period=period_from, course_type=course_type)
                conference_published_list = []

                for conference in conferences:
                    medias = conference.media.all()
                    if medias.count() == 2:
                        if medias[0].is_published or medias[1].is_published:
                            print(conference, conference.public_id)
                            conference_published_list.append(conference)

                for conference in conference_published_list:
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
