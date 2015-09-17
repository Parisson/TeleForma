from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
from django.core.urlresolvers import reverse

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
    help = "Import seminars from a media directory for a special period.name"
    admin_email = 'webmaster@parisson.com'
    args = 'organization period_name log_file media_dir'
    spacer = '_-_'
    original_format = 'webm'
    transcoded_formats = ['mp4', 'ogg', 'mp3']
    image_formats = ['png', 'jpg']
    media_rank_dict = {'bis': 2, 'ter': 3, 'quarter': 4, 'quinquies': 5, 'quater': 4}
    site = Site.objects.get_current()
    id_incr = '40'

    def full_cleanup(self):
        items  = MediaItemTranscoded.objects.all()
        for i in items :
            i.delete()

        items  = MediaItemRelated.objects.all()
        for i in items :
            i.delete()

        items  = MediaItem.objects.all()
        for i in items :
            i.delete()

        items  = MediaCollection.objects.all()
        for i in items :
            i.delete()

        medias = Media.objects.all()
        for media in medias:
            media.delete()

    def delete_media(self, media):
        if media:
            if media.item:
                for trans in media.item.transcoded.all():
                    trans.delete()
                for related in media.item.related.all():
                    related.delete()
                media.item.delete()
            media.delete()

    def seminar_media_cleanup(self, seminar):
        for media in seminar.medias.all():
            seminar.medias.remove(media)
            self.delete_media(media)
        if seminar.media_preview:
            preview = seminar.media_preview
            seminar.media_preview = None
            seminar.save()
            self.delete_media(preview)

    def get_duration(self, file):
        try:
            decoder = timeside.decoder.FileDecoder(file)
            decoder.setup()
            # time.sleep(0.5)
            value = str(datetime.timedelta(0,decoder.input_duration))
            t = value.split(':')
            t[2] = t[2].split('.')[0]
            return ':'.join(t)
        except:
            return '0:0:0'

    def get_item(self, collection, id):
        items = MediaItem.objects.filter(collection=collection, code=id)
        if not items:
            item = MediaItem(collection=collection, code=id)
            item.save()
        else:
            item = items[0]
        return item

    def handle(self, *args, **options):
        organization_name = args[0]
        period_name = args[1]
        log_file = args[2]
        media_dir = args[3]
        domain = args[4]
        logger = Logger(log_file)

        self.site.domain = domain
        self.site.save()

        organization = Organization.objects.get(name=organization_name)
        period = Period.objects.get(name=period_name)
        self.media_dir = media_dir
        file_list = []
        seminars = []

        # NOT FOR PROD : CLEANUP
        # self.cleanup()
        #for seminar in Seminar.objects.filter(period=period):
        #    self.seminar_media_cleanup(seminar)

        walk = os.walk(self.media_dir, followlinks=True)

        for root, dirs, files in walk:
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]
                root_list = root.split(os.sep)

                if ext in self.original_format and not 'preview' in root_list \
                            and not 'preview' in filename and not 'Preview' in filename and filename[0] != '.':

                    print root + os.sep + filename
                    # seminar_rank <= 9
                    seminar_rank = int(root_list[-1][0])

                    if len(root_list[-1]) != 1:
                        rank = root_list[-1][1:]
                        media_rank = self.media_rank_dict[rank.replace('_', '')]
                        preview_trigger = False
                    else:
                        rank = 0
                        media_rank = 1
                        preview_trigger = True

                    course_code = root_list[-2]
                    period_dir = root_list[-3]
                    master_dir = root_list[-4]
                    department_name = root_list[-5]
                    organization_name = root_list[-6]

                    dir = os.sep.join(root_list[-6:])
                    path = dir + os.sep + filename

                    seminar_title = '_'.join([course_code, str(seminar_rank)])
                    collection_id = '_'.join([department_name, seminar_title])
                    course = Course.objects.get(code=course_code)
                    department, c = Department.objects.get_or_create(name=department_name,
                                                                     organization=organization)
                    seminar, c = Seminar.objects.get_or_create(course=course,
                                            rank=seminar_rank, period=period)
                    if c:
                        seminar.title = course.title
                        seminar.status = 1
                        seminar.save()

                    # for media in seminar.medias.all():
                    #     seminar.medias.remove(media)
                    #     media.item.delete()
                    #     media.delete()

                    collections = MediaCollection.objects.filter(code=collection_id)
                    if not collections:
                        collection = MediaCollection(code=collection_id,title=collection_id)
                        collection.save()
                    else:
                        collection = collections[0]

                    id = '_'.join([period.name, self.id_incr, collection_id, ext, str(media_rank)])
                    item = self.get_item(collection, id)
                    item.title = name

                    if not item.file == path:
                        logger.logger.info(seminar.public_url())
                        logger.logger.info(path)
                        if not seminar in seminars:
                            seminars.append(seminar)

                        item.file = path
                        if os.path.getsize(root+os.sep+filename):
                            item.approx_duration = self.get_duration(root+os.sep+filename)
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
                                logger.logger.info(r_path)
                            elif extension[1:] in self.transcoded_formats:
                                t, c = MediaItemTranscoded.objects.get_or_create(item=item, file=r_path)
                                logger.logger.info(r_path)
                            elif extension[1:] == 'kdenlive':
                                related, c = MediaItemRelated.objects.get_or_create(item=item, file=r_path)
                                markers = related.parse_markers(from_first_marker=True)
                                if markers:
                                    for marker in markers:
                                        if float(marker['time']) != 0:
                                            item.title = marker['comment']
                                            item.save()
                                            break
                                logger.logger.info(r_path)

                        media, c = Media.objects.get_or_create(item=item, course=course, type=ext)
                        if c:
                            media.set_mime_type()
                            media.rank = media_rank
                            media.is_published = True
                            media.save()

                        if not media in seminar.medias.all():
                            seminar.medias.add(media)

                        # import previews
                        if preview_trigger:
                            dir = os.path.abspath(root + '/../preview/' +  str(seminar_rank))
                            if os.path.exists(dir):
                                r_dir = os.sep.join(dir.split(os.sep)[-7:])
                                files = os.listdir(dir)
                                code = item.code + '_preview'
                                title = item.title + ' (preview)'
                                item = self.get_item(collection, code)
                                item.title = title
                                item.save()
                                for file in files:
                                    r_path = r_dir + os.sep + file
                                    filename, extension = os.path.splitext(file)
                                    if extension[1:] in self.original_format and not '.' == filename[0]:
                                        item.file = r_path
                                        if os.path.getsize(dir+os.sep+file):
                                            item.approx_duration = self.get_duration(dir+os.sep+file)
                                        item.save()
                                        logger.logger.info(r_path)
                                    elif extension[1:] in self.transcoded_formats:
                                        t, c = MediaItemTranscoded.objects.get_or_create(item=item, file=r_path)
                                        logger.logger.info(r_path)

                                media = Media(item=item, course=course, type=ext)
                                media.set_mime_type()
                                media.is_published = True
                                media.save()
                                seminar.media_preview = media
                                seminar.save()

        for s in seminars:
            print 'http://' + self.site.domain + reverse('teleforma-seminar-detail', kwargs={'pk': s.id})