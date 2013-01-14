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
    help = "Import seminars from the MEDIA_ROOT directory "
    admin_email = 'webmaster@parisson.com'
    args = 'organization log_file'
    spacer = '_-_'
    original_format = 'webm'
    transcoded_formats = ['mp4', 'ogg', 'mp3']
    image_formats = ['png', 'jpg']
    media_rank_dict = {'bis': 2, 'ter': 3, 'quarter': 4, 'quinquies': 5, 'quater': 4}

    def cleanup(self):
        items  = MediaItemTranscoded.objects.all()
        for i in items :
            i.delete()

        items  = MediaItemRelated.objects.all()
        for i in items :
            i.delete()

        items  = MediaItem.objects.all()
        for i in items :
            i.delete()
        
        medias = Media.objects.all()
        for media in medias:
            media.delete()
        
    def handle(self, *args, **options):
        organization_name = args[0]
        log_file = args[1]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        self.media_dir = settings.MEDIA_ROOT + organization.name
        file_list = []
        i = 1

        self.cleanup()

        walk = os.walk(self.media_dir, followlinks=True)

        for root, dirs, files in walk:
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]
                print filename
                root_list = root.split(os.sep)

                if ext in self.original_format and not 'preview' in root_list \
                            and not 'preview' in filename:
                                        # seminar_rank <= 9
                    seminar_rank = int(root_list[-1][0])
                    if len(root_list[-1]) != 1:
                        media_rank = self.media_rank_dict[root_list[-1][1:]]
                    else:
                        media_rank = 1

                    course_code = root_list[-2]
                    master_dir = root_list[-3]
                    department_name = root_list[-4]
                    organization_name = root_list[-5]

                    dir = os.sep.join(root_list[-5:])
                    path = dir + os.sep + filename

                    seminar_title = '_'.join([course_code, str(seminar_rank)])
                    collection_id = '_'.join([department_name, seminar_title])
                    course = Course.objects.get(code=course_code)
                    department, c = Department.objects.get_or_create(name=department_name,
                                                                     organization=organization)
                    seminar, c = Seminar.objects.get_or_create(course=course, rank=seminar_rank)
                    exist = False

                    medias = seminar.medias.all()
                    for media in medias:
                        if media.item.file == path:
                            exist = True
                            break

                    if not exist:
                        collections = MediaCollection.objects.filter(code=collection_id)
                        if not collections:
                            collection = MediaCollection(code=collection_id,title=collection_id)
                            collection.save()
                        else:
                            collection = collections[0]

                        id = '_'.join([collection_id, ext, str(i)])

                        items = MediaItem.objects.filter(collection=collection, code=id)
                        if not items:
                            item = MediaItem(collection=collection, code=id)
                            item.save()
                        else:
                            item = items[0]

                        item.title = name
                        item.file = path

                        decoder = timeside.decoder.FileDecoder(root+os.sep+filename)
                        decoder.setup()
                        time.sleep(0.5)
                        value = str(datetime.timedelta(0,decoder.input_duration))
                        t = value.split(':')
                        t[2] = t[2].split('.')[0]
                        t = ':'.join(t)
                        item.approx_duration = t
                        item.save()
                        
                        files = os.listdir(root)
                        for file in files:
                            r_path = dir + os.sep + file
                            filename, extension = os.path.splitext(file)
                            if extension[1:] in self.image_formats:
                                related, c = MediaItemRelated.objects.get_or_create(item=item, file=r_path)
                                related.title = 'preview'
                                related.set_mime_type()
                                related.save()
                                print 'thumb added'
                            elif extension[1:] in self.transcoded_formats:
                                t, c = MediaItemTranscoded.objects.get_or_create(item=item, file=r_path)
                            elif extension[1:] == 'kdenlive':
                                related, c = MediaItemRelated.objects.get_or_create(item=item, file=r_path)
                                related.save()
                                related.parse()

                        media, c = Media.objects.get_or_create(item=item, course=course, type=ext)
                        if c:
                            media.set_mime_type()
                            media.rank = media_rank
                            media.is_published = True
                            media.save()
                            
                        if not media in seminar.medias.all():
                            seminar.medias.add(media)
                            
                        logger.logger.info(path)
                        i += 1
