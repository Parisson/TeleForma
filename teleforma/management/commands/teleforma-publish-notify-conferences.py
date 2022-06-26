# -*- coding: utf-8 -*-

from optparse import make_option
import logging
import os
from copy import deepcopy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from teleforma.models import *
from teleforma.models.notification import notify


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
    help = """Publish conferences and notify users when \
            conference.date_publish is equal or greater \
            than current date """

    message = "Nouvelle conférence"

    def handle(self, *args, **options):
        conferences = Conference.objects.filter(notified=False,
                        date_publish__lte=datetime.datetime.now())

        for conference in conferences:
            conference.status = 3
            conference.save()

            students = Student.objects.filter(period=conference.period)
            for student in students:
                courses = get_courses(student.user, period=conference.period)
                for course in courses:
                    if conference.course == course['course'] and \
                        conference.course_type in course['types']:
                        media = conference.media.filter(mime_type__in='video')[0]
                        url = reverse('teleforma-media-detail', args=[conference.period.id, media.id])
                        notify(student.user, self.message, url)

            conference.notified = True
            conference.save()