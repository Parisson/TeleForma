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
    help = "Upload conferences media file to s3"
    admin_email = 'webmaster@parisson.com'
    args = 'organization departement log_file'
    spacer = '_-_'
    media_formats = ['mp4', 'mp3']
    image_formats = ['png', 'jpg']

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def find_format(self, conf_dir, file_format):
        files = os.listdir(conf_dir)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext[1:] in file_format:
                return conf_dir + os.sep + file

    def handle(self, *args, **options):
        organization_name = args[0]
        department_name = args[1]
        period_name = args[2]
        log_file = args[3]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(name=department_name,
                                            organization=organization)
        period = Period.objects.get(name=period_name, department=department)
        conferences = Conference.objects.filter(
            department=department,
            period=period,
            imported=True,
            streaming=False)

        for conference in conferences:
            for media in conference.media.all():
                if media.file:
                    filename = os.path.split(media.file.path)[1]
                    with open(media.file.path, 'rb') as f:
                        media.file_s3.save(filename, File(f))
                    media.save()
                    logger.logger.info(media)

