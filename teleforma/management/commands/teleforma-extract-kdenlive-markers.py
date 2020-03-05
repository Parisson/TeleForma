from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from telemeta.util.kdenlive.session import KDEnLiveSession

class Command(BaseCommand):
    help = "Extract markers from a KDEnlive file"
    admin_email = 'webmaster@parisson.com'
    args = 'media_file'

    def handle(self, *args, **options):
        media_file = args[0]
        session = KDEnLiveSession(media_file)
        for mark in session.markers():
            print mark['session_timecode'], mark['time'], mark['comment']
        
