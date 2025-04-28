# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ...models.core import Conference
from teleforma.webclass.models import *



class Command(BaseCommand):
    help = "Store record id for conferences"

    def handle(self, *args, **options):
        bbb = BBBServer.objects.get(pk=2).get_instance()

        missing_records = WebclassRecord.objects.filter(record_id__isnull=True, room_id__isnull=False)

        for record in missing_records:
            recordings = bbb.get_recordings(record.room_id).get_field('recordings')
            if hasattr(recordings, 'get'):
                recordings = recordings['recording']
            if type(recordings) is XMLDictNode:
                recordings = [recordings]
            if recordings:
                # get last session id from the same course
                record.record_id = recordings[0]['recordID']

                print("Add record id %s for webclass record %s" % (record.record_id, record.id))
                record.save()