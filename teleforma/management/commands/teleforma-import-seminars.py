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
    audio_formats = ['ogg', 'mp3']
    video_formats = ['webm', 'mp4']
    image_formats = ['png', 'jpg']
    media_rank_dict = {'bis': 2, 'ter': 3, 'quarter': 4, 'quinquies': 5, 'quater': 4}

    def cleanup(self):
        medias = MediaPackage.objects.all()
        for media in medias:
            for m in media.video.all():
                m.delete()
            for m in media.audio.all():
                m.delete()
            media.delete()
        related = MediaItemRelated.objects.all()
        for r in related:
            r.delete()

    def handle(self, *args, **options):
        organization_name = args[0]
        log_file = args[1]
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        self.media_dir = settings.MEDIA_ROOT + organization.name
        print self.media_dir
        file_list = []
        i = 1

        self.cleanup()

        for root, dirs, files in os.walk(self.media_dir, followlinks=True):
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]
                print filename
                root_list = root.split(os.sep)

                if (ext in self.video_formats or ext in self.audio_formats) \
                        and not 'preview' in root_list and not 'preview' in filename:
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
                    print str(seminar.id)
                    exist = False

                    media_packages = seminar.media.all()
                    for media_package in media_packages:
                        for media in media_package.video.all():
                            if media.item.file == path:
                                exist = True
                                break
                        for media in media_package.audio.all():
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

                        print path
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
                            filename, extension = os.path.splitext(file)
                            if extension[1:] in self.image_formats:
                                related = MediaItemRelated(item=item)
                                related.file = dir + os.sep + file
                                related.title = 'preview'
                                related.set_mime_type()
                                related.save()
                                print 'thumb added'
                                break

                        media = Media(item=item, course=course, type=ext)
                        media.set_mime_type()
                        media.is_published = True
                        media.save()
                        
                        media_package_exist = False
                        media_packages = seminar.media.all()
                        for media_package in media_packages:
                            if media_package.rank == media_rank:
                                media_package_exist = True
                                break
                        
                        if not media_package_exist:
                            media_package = MediaPackage(rank=media_rank, title=seminar_title)
                            media_package.save()
                            seminar.media.add(media_package)

                        if ext in self.video_formats:
                            media_package.video.add(media)
                        if ext in self.audio_formats:
                            media_package.audio.add(media)

                        media_package.is_published = True
                        media_package.save()

                        logger.logger.info(path)
                        i += 1
