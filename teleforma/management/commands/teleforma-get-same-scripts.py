from django.core.management.base import BaseCommand
from teleforma.exam.models import Script
from teleforma.models import Period
from teleforma.models.messages import StudentGroup
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Get all users having uploaded the same script filename"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        period_name = args[0]
        group_name = args[1]
        period = Period.objects.get(name=period_name)
        users = []
        scripts = []
        ss = Script.objects.filter(period=period)
        for script in ss:
            sss = ss.filter(file=script.file).exclude(id=script.id)
            for s in sss:
                if not s in scripts:
                    scripts.append(s)
                    if not s.author in users:
                        users.append(s.author)
        group = StudentGroup(name=group_name)
        group.save()
        for u in users:
            students = u.student.all()
            if students:
                student = students[0]
                group.students.add(student)

