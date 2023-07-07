from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from teleforma.models import *
from django.urls import reverse
from django.core.mail import send_mail

import logging
import os, sys, time, datetime


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
    email_subject="[Pro-Barreau] import media STAGING"
    to_emails=['webmaster@parisson.com',
        'jeannot@parisson.com',
        'kostya.rilov@pre-barreau.com'
        ]
    from_email = 'no-reply@pro-barreau.com'
    original_format = ['mp4']
    transcoded_formats = ['mp3',]
    image_formats = ['png', 'jpg']
    media_rank_dict = {'bis': 2, '1bis': 2, '1ter': 3, 'ter': 3, 'quarter': 4, '1quater': 4, 'quinquies': 5, 'quater': 4, 'sexies': 6, 'septies': 7, 'sexsies': 6, 'octies': 8}

    site = Site.objects.get(id=settings.SITE_ID)
    id_incr = '40'
    size_limit = 16384

    def add_arguments(self, parser):
        parser.add_argument('--organization-name', type=str, required=True,
                            help='organization name')
        parser.add_argument('--logfile', type=str, required=True,
                            help='log file path')
        parser.add_argument('--period-name', type=str, required=True,
                            help='period name')
        parser.add_argument('--media-dir', type=str, required=True,
                            help='media dir')
        parser.add_argument('--delete', type=bool,
                            help='delete all media before import')

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
        organization_name = options['organization_name']
        period_name = options['period_name']
        media_dir = options['media_dir']
        log_file = options['logfile']
        delete = options['delete']
        logger = Logger(log_file)

        organization = Organization.objects.get(name=organization_name)
        period = Period.objects.get(name=period_name)
        self.media_dir = media_dir
        file_list = []
        seminars = []

        # NOT FOR PROD : CLEANUP
        # self.cleanup()
        # for seminar in Seminar.objects.filter(period=period):
            # self.seminar_media_cleanup(seminar)

        walk = os.walk(self.media_dir, followlinks=True)

        for root, dirs, files in walk:
            for filename in files:
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]
                root_list = root.split(os.sep)
                path = root + os.sep + filename
                statinfo = os.stat(path)

                if ext in self.original_format and not 'preview' in root_list \
                        and not 'preview' in filename and not 'Preview' in filename and filename[0] != '.' \
                        and statinfo.st_size > self.size_limit:

                    seminar_rank = root_list[-1]
                    #print(seminar_rank)
                    if seminar_rank.isdigit():
                       media_rank_offset = 0
                    elif seminar_rank[0:2].isdigit():
                       seminar_rank = root_list[-1][0:2]
                       media_rank_offset = 2
                    elif seminar_rank[0:1].isdigit():
                       seminar_rank = root_list[-1][0:1]
                       media_rank_offset = 1

                    seminar_rank = int(seminar_rank)
                    #print(seminar_rank)

                    # seminar_rank <= 9 
                    #seminar_rank = int(root_list[-1][0])
                    if '-' in root_list[-1]:
                        seminar_rank, media_rank = root_list[-1].split('-')
                        preview_trigger = False
                    elif media_rank_offset:
                        rank = root_list[-1][media_rank_offset:]
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
                    course = Course.objects.get(code=course_code)
                    department, c = Department.objects.get_or_create(name=department_name,
                                                                     organization=organization)
                    #ss = Seminar.objects.filter(course=course,
                    #                        rank=seminar_rank, period=period)
                    #print([s.id for s in ss])
                    
                    #print(course, seminar_rank, period)
                    seminar, c = Seminar.objects.get_or_create(course=course,
                                            rank=seminar_rank, period=period,
                                            magistral=False)
                    if c:
                        seminar.title = course.title
                        seminar.status = 1
                        seminar.save()
                    
                    # if not item.file == path and not items_webm:
                    #logger.logger.info(seminar.public_url())
                    #logger.logger.info(path)

                    # cleanup old media
                    #print(delete)

                    if delete:
                        for media in seminar.medias.all():
                            seminar.medias.remove(media)

                    #print(path)
                    
                    medias = Media.objects.filter(course=course, file=path, type=ext)
                    if medias.count() >= 1:
                        c = False
                    else:
                        media, c = Media.objects.get_or_create(course=course, file=path, type=ext)

                    if c:
                        #print(path)
                        if not seminar in seminars:
                            seminars.append(seminar)

                        media.set_mime_type()
                        media.rank = media_rank
                        media.is_published = True
                        media.save()

                        if not media in seminar.medias.all():
                            seminar.medias.add(media)

                        files = os.listdir(root)
                        for file in files:
                            r_path = dir + os.sep + file
                            filename, extension = os.path.splitext(file)
                            if extension[1:] in self.image_formats:
                                media.poster_file = r_path
                                print(r_path)
                            elif extension[1:] in self.transcoded_formats and not extension[1:] in self.original_format:
                                transcoded, c = MediaTranscoded.objects.get_or_create(item=media, file=r_path)
                            elif extension[1:] == 'kdenlive':
                                media.session_file = r_path
                                print(r_path)
                                media.parse_markers(from_first_marker=False)
                            logger.logger.info(r_path)
                        media.save()

                        # import previews
                        if preview_trigger:
                            dir = os.path.abspath(root + '/../preview/' +  str(seminar_rank))
                            if os.path.exists(dir):
                                r_dir = os.sep.join(dir.split(os.sep)[-7:])
                                files = os.listdir(dir)

                                if files and seminar.media_preview:
                                    seminar.media_preview.delete()

                                media_preview, c = Media.objects.get_or_create(course=course,
                                                                        type=ext,
                                                                        title='preview')
                                if c:
                                    media_preview.set_mime_type()
                                    media_preview.rank = media_rank
                                    media_preview.is_published = True
                                    media_preview.save()

                                for file in files:
                                    r_path = r_dir + os.sep + file
                                    filename, extension = os.path.splitext(file)
                                    if extension[1:] in self.image_formats:
                                        media_preview.poster_file = r_path
                                    if extension[1:] in self.original_format and not '.' == filename[0]:
                                        media_preview.file = r_path
                                        logger.logger.info(r_path)
                                    elif extension[1:] in self.transcoded_formats:
                                        transcoded, c = MediaTranscoded.objects.get_or_create(item=media_preview, file=r_path)
                                        logger.logger.info(r_path)

                                media_preview.save()
                                media_preview.set_mime_type()
                                media_preview.is_published = True
                                media_preview.save()
                                seminar.media_preview = media_preview
                                seminar.save()

        for s in seminars:
            url = 'https://' + self.site.domain + reverse('teleforma-seminar-detail', kwargs={'pk': s.id})
            print(url)
            logger.logger.info(url)

        log = open(log_file, 'r')
        log_txt = log.read()
        log.close()
        send_mail(
            self.email_subject,
            log_txt,
            self.from_email,
            self.to_emails,
            fail_silently=False,
        )
