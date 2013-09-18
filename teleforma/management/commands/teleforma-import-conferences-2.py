from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import os, sys, time, datetime
import timeside


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('teleforma')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Import original and transcoded conference media from the MEDIA_ROOT directory "
    admin_email = 'webmaster@parisson.com'
    args = 'organization log_file'
    spacer = '_-_'
    original_format = 'webm'
    transcoded_formats = ['mp4', 'ogg', 'mp3']
    image_formats = ['png', 'jpg']
    ffmpeg_args = {'mp3' : ' -vn -acodec libmp3lame -aq 6 -ac 2 ',
                    'ogg' : ' -vn -acodec copy ',
                    'mp4' : ' -vcodec libx264 -r 24 -b 512k -threads 4 -acodec libfaac -ar 48000 -ab 96k -ac 2 ',
              }

    def cleanup(self):
        items  = MediaItemTranscoded.objects.all()
        for item in items:
            item.delete()
        items = Media.objects.all()
        for item in items:
            item.delete()
        items = MediaItem.objects.all()
        for item in items:
            item.delete()
        items  = MediaCollection.objects.all()
        for i in items :
            i.delete()
        
    def get_duration(self, file):
        decoder = timeside.decoder.FileDecoder(file)
        decoder.setup()
        # time.sleep(0.5)
        value = str(datetime.timedelta(0,decoder.input_duration))
        t = value.split(':')
        t[2] = t[2].split('.')[0]
        return ':'.join(t)


    def handle(self, *args, **options):
        organization_name = args[0]
        log_file = args[1]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        self.media_dir = settings.MEDIA_ROOT + organization.name
        file_list = []

#        self.cleanup()

        for root, dirs, files in os.walk(self.media_dir, followlinks=True):
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]

                if ext and ext in self.original_format and name[0] != '.':
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
                    conferences = Conference.objects.filter(public_id=public_id)
                    if conferences:
                        conference = conferences[0]

                        exist = False
                        medias = conference.media.all()
                        for media in medias:
                            if media.item.file == path:
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

                            # ORIGINAL MEDIA
                            collections = MediaCollection.objects.filter(code=collection_id)
                            if not collections:
                                collection = MediaCollection(code=collection_id,title=collection_id)
                                collection.save()
                            else:
                                collection = collections[0]
                            code = '_'.join([collection_id, public_id, ext])
                            items = MediaItem.objects.filter(collection=collection, code=code)
                            if not items:
                                item = MediaItem(collection=collection, code=code)
                                item.save()
                            else:
                                item = items[0]
                            item.title = name
                            item.file = path
                            #item.approx_duration = self.get_duration(root+os.sep+filename)
                            item.save()

                            # IMAGES
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

                            # TRANSCODED MEDIA
                            for format in self.ffmpeg_args.keys():
                                filename = name + '.' + format
                                dest = os.path.abspath(root + os.sep + filename)
                                r_path = dir + os.sep + filename
                                # if not os.path.exists(dest):
                                #     command = 'ffmpeg -i ' + path + ffmpeg_args[format] + ' -y ' + dest
                                #     os.system(command)
                                t, c = MediaItemTranscoded.objects.get_or_create(item=item, file=r_path)

                            media = Media(conference=conference)
                            media.item = item
                            media.course = conference.course
                            media.course_type = conference.course_type
                            media.period = conference.period
                            media.type = ext
                            media.set_mime_type()
                            media.save()
                            conference.save()
                            logger.logger.info(path)
