
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import translation
from django.conf import settings
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.exam.models import *
import logging
import codecs
import time, os


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
    help = "submit all script to Box View"
    args = "log_file"

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        logger = Logger(args[0])
        for script in Script.objects.filter(status=2):
            logger.logger.info(script.title)
            logger.logger.info(str(script.id) + ' : ' + script.url)
            if not script.file:
                logger.logger.error('No file!')
            script.submit()
            logger.logger.info(script.status)
            time.sleep(10)

