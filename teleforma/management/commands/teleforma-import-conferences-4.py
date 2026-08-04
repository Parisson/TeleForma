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
    help = "Import conferences from the MEDIA_ROOT directory "
    admin_email = 'webmaster@parisson.com'
    args = 'organization log_file'
    spacer = '_-_'
    media_formats = ['mp4', 'mp3']
    image_formats = ['png', 'jpg']
    webm_pattern = "_0.webm"
    mp3_pattern = ".mp3-"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def find_format(self, conf_dir, file_format):
        files = []
        all_files = os.listdir(conf_dir)
        for file in all_files:
            name, ext = os.path.splitext(file)
            if ext[1:] in file_format:
                files.append(conf_dir + os.sep + file)
        if len(files) > 1:
            for file in files:
                if self.webm_pattern in file or self.mp3_pattern in file:
                    return file
        elif len(files) == 1:
            return files[0]
        else:
            return ""

    def handle(self, *args, **options):
        organization_name = args[0]
        department_name = args[1]
        log_file = args[2]
        logger = Logger(log_file)
        file_list = []

        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(name=department_name,
                                            organization=organization)
        media_dir = settings.MEDIA_ROOT + organization.name + os.sep + department_name
        conferences = Conference.objects.filter(
            department=department,
            imported=False,
            streaming=False)

        for conference in conferences:
            conf_dir = os.sep.join([
                media_dir,
                str(conference.date_begin.year),
                self.spacer.join([
                    conference.course.code,
                    "-".join(str(conference.course_type).split(" "))
                    ]),
                conference.public_id])

            if (os.path.exists(conf_dir) and not conference.media.all()):

                for image_format in self.image_formats:
                    poster_file = self.find_format(conf_dir, image_format)

                for media_format in self.media_formats:
                    media_file = self.find_format(conf_dir, media_format)
                    media = Media(conference=conference)
                    media.course = conference.course
                    media.period = conference.period
                    media.course_type = conference.course_type
                    media.type = media_format
                    media.is_published = False

                    media.file = media_file.replace(settings.MEDIA_ROOT, "")
                    media.save()
                    filename = os.path.split(media_file)[1]
                    with open(media_file, 'rb') as f:
                        media.file_s3.save(filename, File(f))
                    media.save()
                    media.set_mime_type()
                    conference.imported = True
                    logger.logger.info(media_file)

                    media.poster_file = poster_file.replace(settings.MEDIA_ROOT, "")
                    media.save()
                    filename = os.path.split(poster_file)[1]
                    with open(poster_file, 'rb') as f:
                        media.poster_file_s3.save(filename, File(f))
                    media.save()
                    conference.s3_exported = True
                    logger.logger.info(poster_file)

                conference.imported = True
                conference.save()

