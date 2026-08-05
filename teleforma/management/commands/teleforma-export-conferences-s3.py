from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.base import ContentFile
from teleforma.models import *
import logging
import os


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
    help = "Export old conferences to S3 and delete local conf dir"
    admin_email = 'webmaster@parisson.com'
    args = 'organization department period log_file'
    spacer = '_-_'
    media_formats = ['mp4', 'mp3']
    image_formats = ['png', 'jpg']
    webm_pattern = "_0.webm"
    mp3_pattern = ".mp3-"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        organization_name = args[0]
        department_name = args[1]
        year = args[2]
        log_file = args[3]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(name=department_name,
                                            organization=organization)
        periods = Period.objects.filter(name__icontains=year)
        media_dir = settings.MEDIA_ROOT + organization.name + os.sep + department_name

        for period in periods:
            conferences = Conference.objects.filter(
                department=department,
                period=period,
                s3_exported=False,
                status=3,
                )
            for conference in conferences:
                for media in conference.media.all():

                    media_file = media.file.path
                    filename = os.path.split(media_file)[1]
                    with open(media_file, 'rb') as f:
                        media.file_s3.save(filename, File(f))
                    media.set_mime_type()
                    media.save()
                    logger.logger.info(media_file)

                    poster_file = media.poster_file.path
                    filename = os.path.split(poster_file)[1]
                    with open(poster_file, 'rb') as f:
                        media.poster_file_s3.save(filename, File(f))
                    media.save()
                    logger.logger.info(poster_file)

                    conference.s3_exported = True
                    conference.save()

