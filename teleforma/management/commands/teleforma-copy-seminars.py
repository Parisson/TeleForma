from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from django.utils import translation
from django.core.urlresolvers import reverse
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import datetime

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
    help = """Copy some seminars and their content thanks to their expiry date year"""
    args = ['site_domain from_year to_year log_file']
    language_code = 'fr_FR'
    more = ['deontologie_1', 'deontologie_2', 'commercial_2', 'Contrats_4', 'PAC_5']
    site = Site.objects.get_current()

    def handle(self, *args, **kwargs):
        to_year = int(args[-2])
        from_year = int(args[-3])
        logger = Logger(args[-1])
        domain = args[-4]

        self.site.domain = domain
        self.site.save()

        to_period, c = Period.objects.get_or_create(name=str(to_year))
        from_period, c = Period.objects.get_or_create(name=str(from_year))
        expiry_date = datetime.datetime(2014, 12, 31)

        for seminar in Seminar.objects.all():
            if seminar.expiry_date:
                if seminar.expiry_date.date() == expiry_date.date() \
                  or (seminar.period == from_period and seminar.code in self.more):
                    seminar.period = from_period
                    seminar.save()
                    clone = seminar.clone()
                    clone.publish_date = seminar.publish_date.replace(year=to_year)
                    clone.expiry_date = seminar.expiry_date.replace(year=to_year)
                    clone.period = to_period
                    clone.status = 1
                    clone.save()
                    log = 'new seminar:' + unicode(clone)
                    logger.logger.info(log)
                    print log
                    log = 'http://' + self.site.domain + reverse('teleforma-seminar-detail', kwargs={'pk': clone.id})
                    logger.logger.info(log)
                    print log

                    for field in seminar._meta.many_to_many:
                        if field.rel.to == Document:
                            source = getattr(seminar, field.attname)
                            destination = getattr(clone, field.attname)

                            for item in source.all():
                                item.period = from_period
                                item.save()
                                item_clone = item.clone()
                                item_clone.readers = []
                                item_clone.period = to_period
                                item_clone.save()
                                destination.remove(item)
                                destination.add(item_clone)
                                # print ("media cloned and assigned:", item_clone)

                    for question in seminar.question.all():
                        question_clone = question.clone()
                        question_clone.seminar = clone
                        question_clone.save()
                        # print ("question cloned and assigned:", question_clone)


