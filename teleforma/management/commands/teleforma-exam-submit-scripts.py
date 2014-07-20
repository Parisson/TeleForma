
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
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
        logger = Logger(args[0])
        for script in Script.objects.filter(status=2):
            logger.logger.info(script.title)
            if script.file:
            	if os.path.exists(script.file.path):
	                script.fix_filename()
	                try:
	                    script.submit()
	                except:
	                    logger.logger.error('ERROR')
	                logger.logger.info('OK')
	                time.sleep(30)
            else:
            	logger.logger.error('No file!')

