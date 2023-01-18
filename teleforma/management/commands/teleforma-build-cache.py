
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.conf import settings
from teleforma.models.crfpa import Student
import logging

from teleforma.views.core import get_courses


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        if file:
            self.hdlr = logging.FileHandler(file)
        else:
            self.hdlr = None
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        if self.hdlr:
            self.hdlr.setFormatter(self.formatter)
            self.logger.addHandler(self.hdlr)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = "Build get_courses cache"

    def add_arguments(self, parser):
        parser.add_argument('--logfile', type=str, required=False,
                            help='log file to use')

    def handle(self, *args, **options):
        logpath = options['logfile']
        logger = Logger(logpath)

        total = Student.objects.filter(user__is_active=True).count()
        logger.logger.info(f'Found {total} active students...')
        for i, student in enumerate(Student.objects.filter(user__is_active=True, platform_only=True)):
            if i % 100 == 0:
                logger.logger.info(f"build cache : {int(i * 100 / total)}%")
            periods = [training.period for training in student.trainings.all()]
            for period in periods:
                for child in period.children.all():
                    periods.append(child)
            for period in periods + [None]:
                # for date_order in (True, False):
                #     for num_order in (True, False):
                #         for num_courses in (True, False):
                            # logger.logger.info(f"build cache for get_courses-{student.user.id}-{date_order}-{num_order}-{num_courses}-{period and period.id or None}")
                get_courses(student.user, period=period)
