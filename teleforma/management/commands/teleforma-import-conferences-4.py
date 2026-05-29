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

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        organization_name = args[0]
        department_name = args[1]
        log_file = args[2]
        logger = Logger(log_file)
        file_list = []
        i = 1

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
                    conference.course.course_type]),
                conference.public_id])

            if os.path.exists(conf_dir):
                files = os.listdir(conf_dir)

                for media_format in media_formats:
                    media = Media(conference=conference)
                    media.course = conference.course
                    media.period = conference.period
                    media.course_type = conference.course_type
                    media.type = media_format
                    media.is_published = False

                    for file in files:
                        name, ext = os.path.splitext(file)
                        full_path = conf_dir + os.sep + file
                        rel_path = full_path.replace(settings.MEDIA_ROOT, "")

                        # POSTER
                        if ext[1:] in self.image_formats:
                            media.poster_file = rel_path
                            break

                        # MEDIA FILE
                        if ext[1:] in self.media_formats:
                            media.file = rel_path
                            media.save()
                            filename = os.path.split(full_path)[1]
                            with open(full_path, 'rb') as f:
                                media.file_s3.save(filename, File(f))
                            media.set_mime_type()
                            media.save()

                conference.imported = True
                conference.save()

                logger.logger.info(path)
                i += 1

