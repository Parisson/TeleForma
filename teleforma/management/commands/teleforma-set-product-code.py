from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from teleforma.models import *


class Command(BaseCommand):
    help = "Set missing product code on 2020+ seminars / conferences. One shot script."
    args = ''

    def handle(self, *args, **options):

        sems = {}
        for seminar in Seminar.objects.filter(period__name=2020):
            print(seminar)
            seminar.save()
            sems[seminar.title] = seminar.product_code

        for seminar in Seminar.objects.filter(period__name=2021):
            seminar.product_code = sems.get(seminar.title)
            seminar.save()


        confs = {}
        for conference in Conference.objects.filter(period__name=2020):
            print(conference)
            conference.save()
            confs[conference.title] = conference.product_code


        for conference in Conference.objects.filter(period__name=2021):
            conference.product_code = confs.get(conference.title)
            conference.save()


        
        
