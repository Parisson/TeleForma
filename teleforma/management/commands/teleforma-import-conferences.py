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
    args = 'organization log_file'
    spacer = '_-_'
    media_formats = ['mp3', 'webm']
    image_formats = ['png', 'jpg']


    def cleanup(self):
        medias = Media.objects.all()
        for media in medias:
            media.delete()
        items = MediaItem.objects.all()
        for item in items:
            item.delete()

    def handle(self, *args, **options):
        organization_name = args[0]
        log_file = args[1]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        self.media_dir = settings.MEDIA_ROOT + organization.name
        file_list = []
        all_conferences = Conference.objects.all()
        i = 1

#        self.cleanup()

        for root, dirs, files in os.walk(self.media_dir):
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]

                if ext in self.media_formats:
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

                    department, c = Department.objects.get_or_create(name=department_name,
                                                                     organization=organization)
                    if Conference.objects.filter(public_id=public_id):
                        conference = Conference.objects.get(public_id=public_id)

                        exist = False
                        medias = conference.media.all()
                        for media in medias:
                            if media.item.file == path:
                                exist = True
                                break

                        streaming = False
                        try:
                            stations = conference.station.filter(started=True)
                            ids = [station.public_id for station in stations]
                            for id in ids:
                                if id == public_id:
                                    streaming = True
                        except:
                            pass

                        if not exist and not streaming:
                            collections = MediaCollection.objects.filter(code=collection_id)
                            if not collections:
                                collection = MediaCollection(code=collection_id,title=collection_id)
                                collection.save()
                            else:
                                collection = collections[0]

                            id = '_'.join([collection_id, public_id, ext, str(i)])

                            items = MediaItem.objects.filter(collection=collection, code=id)
                            if not items:
                                item = MediaItem(collection=collection, code=id)
                                item.save()
                            else:
                                item = items[0]

                            item.title = name
                            item.file = path
                            item.save()

                            files = os.listdir(root)
                            for file in files:
                                filename, extension = os.path.splitext(file)
                                if extension[1:] in self.image_formats:
                                    related = MediaItemRelated(item=item)
                                    related.file = dir + os.sep + file
                                    related.title = 'preview'
                                    related.set_mime_type()
                                    related.save()
                                    break

                            media = Media(conference=conference)
                            media.item = item
                            media.course = conference.course
                            media.course_type = conference.course_type
                            media.type = ext
                            media.set_mime_type()
                            media.save()
                            conference.save()
                            logger.logger.info(path)
                            i += 1

