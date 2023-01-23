# -*- coding: utf-8 -*-

from optparse import make_option
import logging
import os
from copy import deepcopy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from teleforma.models.core import Conference, ConferencePublication, Period
from teleforma.models.crfpa import Student
from teleforma.models.notification import notify
from teleforma.views.core import get_courses
import datetime


MINUTES_LOW_RANGE = 5
MINUTES_HIGH_RANGE = 25

class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        if file:
            self.hdlr = logging.FileHandler(file)
        else:
            self.hdlr = None
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        if self.hdlr:
            self.hdlr.setFormatter(self.formatter)
            self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Publish conferences and notify users when \
            conference.date_publish is equal or greater \
            than current date """

    def add_arguments(self, parser):
        parser.add_argument('--logfile', type=str, required=False,
                            help='log file to use')

        parser.add_argument('--period', type=str, required=True,
                            help='period to process')

        parser.add_argument('--minute-low-range', type=int, required=False,
                            help='minute low range')

        parser.add_argument('--minute-high-range', type=int, required=False,
                            help='minute high range')

    def handle(self, *args, **options):
        logpath = options['logfile']
        logger = Logger(logpath)


        period_name = options['period']
        period = Period.objects.get(name=period_name)

        minute_low_range = options['minute_low_range']
        if not minute_low_range:
            minute_low_range = MINUTES_LOW_RANGE

        minute_high_range = options['minute_high_range']
        if not minute_high_range:
            minute_high_range = MINUTES_HIGH_RANGE

        print(minute_low_range)
        print(minute_high_range)

        now_minus = datetime.datetime.now() - datetime.timedelta(minutes=minute_low_range)
        now_plus = datetime.datetime.now() + datetime.timedelta(minutes=minute_high_range)

        publications = list(Conference.objects.filter(
                        period=period,
                        status=2,
                        notified=False,
                        date_publish__lte=now_plus,
                        date_publish__gte=now_minus,
                        )) + list(ConferencePublication.objects.filter(
                        period=period,
                        status=2,
                        notified=False,
                        date_publish__lte=now_plus,
                        date_publish__gte=now_minus,
                        ))
        print(publications)
    
        logger.logger.info("Starting conference publication process")

        for publication in publications:
            publication.status = 3

            if type(publication) == ConferencePublication:
                conference = publication.conference
            else:
                conference = publication            
            medias = conference.media.all()
            for media in medias:
                media.is_published = True
                media.save()
            logger.logger.info("Conference published: " + conference.public_id)

            for media in medias:
                if "video/mp4" in media.mime_type:
                    linked_media = media
            media = conference.media.filter(mime_type='video/mp4')[0]
            url = reverse('teleforma-media-detail', args=[conference.period.id, linked_media.id])
            message = "Nouvelle conférence publiée : " + str(conference)

            students = Student.objects.filter(period=publication.period, platform_only=True)
            for student in students:
                try:
                    if student.user:
                        courses = get_courses(student.user, period=publication.period)
                        for course in courses:
                            if conference.course == course['course'] and \
                                    conference.course_type in course['types']:
                                notify(student.user, message, url)
                                logger.logger.info("Student notified: " + student.user.username)
                                print("notify", student)
                except:
                    #logger.logger.info("Student NOT notified: " + str(student.id))
                    print("can't notify", student)
                    continue

            publication.notified = True
            publication.save()
