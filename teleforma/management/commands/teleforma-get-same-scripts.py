from django.core.management.base import BaseCommand
from teleforma.exam.models import Script
from teleforma.models import Period
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Get all users having uploaded the same script filename"

    def handle(self, *args, **options):
        name = args[0]
        period = Period.objects.get(name=name)
        users = []
        scripts = []
        for script in Script.objects.filter(period=period):
            ss = Script.objects.filter(file=script.file)
            for s in ss:
                scripts.append(s)
                users.append(s.author)
        print(users)
