from django.core.management.base import BaseCommand
from teleforma.exam.models import Script
from teleforma.models import Period
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Get all users having uploaded the same script filename"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        name = args[0]
        period = Period.objects.get(name=name)
        users = []
        scripts = []
        ss = Script.objects.filter(period=period)
        for script in ss:
            sss = ss.objects.filter(file=script.file)
            for s in sss:
                scripts.append(s)
                users.append(s.author.username)
        print(users)
