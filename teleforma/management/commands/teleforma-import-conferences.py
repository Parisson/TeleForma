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
    media_dir = settings.MEDIA_ROOT+os.sep+'items'
    spacer = '_-_'
    formats = ['mp3', 'webm']
    logger = Logger('/var/log/telecaster/import.log')

    def handle(self, *args, **options):
        file_list = []
        all_conferences = Conference.objects.all()

        for root, dirs, files in os.walk(self.media_dir):
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1]

                if ext in formats:
                    path = root + os.sep + filename
                    root_list = root.split(os.sep)
                    public_id = root_list[-1]
                    course_id = root_list[-2].split(self.spacer)[0]
                    course_type = root_list[-2].split(self.spacer)[1].lower()
                    department_name = root_list[-3]
                    date = root_list[-4]

                    department, created = Department.objects.get_or_create(name=department_name)
                    conference, created = Conference.objects.get_or_create(public_id=public_id)

                    exist = False
                    medias = conference.media.all()
                    for media in medias:
                        items = media.items.filter(file=path)
                        if items:
                            exist = True
                            break

                    if not exist:
                        collection_id = '_'.join(department_name, course_id, course_type)
                        collection, c = MediaCollection.objects.get_or_create(public_id=collection_id,
                                                            title=collection_id.replace('_', ' - '))
                        item = MediaItem.objects.create(collection=collection,
                                         public_id='_'.join(collection_id, public_id, ext),
                                         title=name,
                                         file=path)
                        media, c = Media.objects.get_or_create(conference=conference)
                        media.items.add(item)
                        logger.info('Imported: ' + path)

