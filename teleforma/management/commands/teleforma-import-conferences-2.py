from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
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
    original_format = ['webm', 'mp4']
    transcoded_formats = ['mp4', 'ogg', 'mp3']
    image_formats = ['png', 'jpg']

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        organization_name = args[0]
        department_name = args[1]
        log_file = args[2]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        department = Department.objects.get(name=department_name,
                                            organization=organization)
        self.media_dir = settings.MEDIA_ROOT + organization.name + os.sep + department_name
        file_list = []
        all_conferences = Conference.objects.all()
        i = 1

        for root, dirs, files in os.walk(self.media_dir):
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]

                if ext and (ext in self.original_format or ext in self.transcoded_formats) and name[0] != '.':
                    root_list = root.split(os.sep)
                    public_id = root_list[-1]
                    course = root_list[-2]
                    course_id = course.split(self.spacer)[0]
                    course_type = course.split(self.spacer)[1].lower()
                    date = root_list[-3]
                    department_name = root_list[-4]
                    organization_name = root_list[-5]
                    dir = os.sep.join(root_list[-5:])
                    path = dir + os.sep + filename
                    collection_id = '_'.join([department_name, course_id, course_type])

                    if Conference.objects.filter(public_id=public_id) and department:
                        conference = Conference.objects.get(public_id=public_id)
                        department = Department.objects.get(name=department_name,
                                                            organization=organization)
                        exist = False
                        medias = conference.media.all()
                        for media in medias:
                            if media.file == path:
                                exist = True
                                break

                        streaming = False
                        try:
                            stations = conference.station.filter(started=True, public_id=public_id)
                            if stations:
                                streaming = True
                        except:
                            pass

                        if not exist and not streaming:
                            media = Media(conference=conference)
                            media.file = path
                            media.course = conference.course
                            media.period = conference.period
                            media.course_type = conference.course_type
                            media.type = ext
                            media.is_published = False
                            media.set_mime_type()

                            files = os.listdir(root)
                            for file in files:
                                filename, extension = os.path.splitext(file)
                                if extension[1:] in self.image_formats:
                                    media.poster_file = dir + os.sep + file
                                    break

                            media.save()
                            conference.save()

                            logger.logger.info(path)
                            i += 1

