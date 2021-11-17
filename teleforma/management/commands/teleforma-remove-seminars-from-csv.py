# -*- coding: utf-8 -*-
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from teleforma.models import *
import datetime
import csv

class Command(BaseCommand):
    help = "Remove conferences from users, from a CSV file"
    args = "path"

    def handle(self, *args, **options):
        """
        Import a CSV
        """
        fname = args[0]
        titlerow = None
        with open(fname) as f:
            for row in csv.reader(f, delimiter=';'):
                if not titlerow:
                    titlerow = row
                else:
                    self.process_row(titlerow, row)

    def process_row(self, title, row):
        """
        Process a row
        """
        email = None
        seminar = None
        todel = []
        for key, val in zip(title, row):
            val = val.strip()
            if key == 'email' and val:
                email = val
            elif key.startswith('séminaire'):
                seminar = val
            elif key in ('commentaires', 'commentaire') and seminar:
                if val == 'non':
                    if not '(' in seminar or not seminar.endswith(')'):
                        print("WARNING: malformed seminar %s" % seminar)
                        continue
                    title, sid = seminar.rsplit('(', 1)
                    sid = sid[:-1]
                    title = title.strip()
                    seminar = list(Seminar.objects.filter(pk = sid)[:1])
                    seminar = seminar and seminar[0]
                    if not seminar:
                        print('WARNING: Seminar %s not found' % sid)
                    wanted_title = str(seminar).strip()
                    if title != wanted_title:
                        print("WARNING: Seminar %s: mismatched title %r %r" % (sid, title, wanted_title))
                    todel.append(seminar)
            else:
                seminar = None

        if not email or not todel:
            return
        
        user = list(User.objects.filter(email = email)[:1])
        user = user and user[0]
        if not user:
            print("WARNING: user %s not found" % email)
            return
        auditor = list(user.auditor.all()[:1])
        auditor = auditor and auditor[0]
        if not auditor:
            print("WARNING: auditor for user %s not found" % email)
            return

        existing = auditor.seminars.all().values('id')
        existing = set([ sem['id'] for sem in existing ])
        
        print("===> ", email)
        for seminar in todel:
            if seminar.pk in existing:
                print seminar
                auditor.seminars.remove(seminar)
            else:
                print("WARNING: seminar %d for user %s not found" % (seminar.pk, email))
                    
