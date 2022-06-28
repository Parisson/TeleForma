from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from teleforma.models import *
from teleforma.bbb_utils import bbb
import sys

import datetime

def as_list(what):
    """
    Ensure something is a list or tuple
    """
    if isinstance(what, (list, tuple)):
        return what
    return [ what ]

class Command(BaseCommand):
    help = "Credit time to students connected to a Big Blue Button webclass"

    def add_arguments(self, parser):
        parser.add_argument('duration', type=int,
                            help='duration in seconds')
        parser.add_argument('--logfile', type=str, required=True,
                            help='log file to use')
        
    
    def handle(self, *args, **options):
        duration = options['duration']
        logpath = options['logfile']
        sys.stdout = open(logpath, 'a', encoding='utf-8')

        end = datetime.datetime.now()
        start = end - datetime.timedelta(seconds = duration)
        print(("=== Starting at %s" % end.strftime('%Y-%m-%d %H:%M:%S')))
        meetings = bbb.get_meetings()
        meetings = meetings.get_field("meetings")
        # no conference in BBB
        if "meeting" not in meetings:
            print("No meeting found")
            return
        meetings = as_list(meetings["meeting"])

        print(("=== Starting at %s (with duration %d)" % (end.strftime('%Y-%m-%d %H:%M:%S'), duration)))

        done = set()
        
        for meeting in meetings:
            meeting_id = str(meeting['meetingID'])
            try:
                conf = Conference.objects.get(webclass_id = meeting_id)
                seminar = Seminar.objects.get(conference = conf)
            except:
                print(("Warning, can't find Seminar for %s" % meeting_id))
                continue

            sem_txt = "%s (%s)" % (seminar, seminar.pk)
            attendees = as_list(meeting['attendees']['attendee'])
            for attendee in attendees:
                user_id = str(attendee['userID'])
                key = (meeting_id, user_id) 
                if key in done:
                    print(("Warning, user %s duplicate for %s" % (user_id, sem_txt)))
                    continue
                done.add(key)
                
                try:
                    user = User.objects.get(username = user_id)
                except:
                    print(("Warning, can't find user %s for seminar %s" % (user_id, sem_txt)))
                    continue
                user_txt = "%s (%s)" % (user, user.pk)
                rev = SeminarRevision.objects.filter(seminar = seminar,
                                                     user = user,
                                                     date_modified = None)
                if rev.count():
                    print(("User %s already has an open revision on %s" % (user_txt, sem_txt)))
                else:                    
                    print(("Crediting %d seconds to %s on %s" % (duration, user_txt, sem_txt)))
                    sr = SeminarRevision(seminar = seminar,
                                         user = user,
                                         date = start,
                                         date_modified = end)
                    sr.save()
                    sr.date = start
                    sr.save()
