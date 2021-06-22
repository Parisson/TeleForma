
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from jqchat.models import Message
import datetime
from teleforma.exam.models import Script
from pdfannotator.models import Annotation, AnnotationComment


class Command(BaseCommand):
    help = "Delete script annotations from previous year"

    def handle(self, *args, **options):
        date_now = datetime.datetime.now()
        date_old = date_now.replace(year=date_now.year-1, month=12, day=31)
        print(date_old)
        scripts = Script.objects.filter(date_submitted__lte=date_old)
        print(scripts.count())

        for script in scripts:
            annotations = Annotation.objects.filter(uuid=script.uuid)
            for annotation in annotations:
                annotation.delete()
            annotation_comments = AnnotationComment.objects.filter(uuid=script.uuid)
            for annotation_comment in annotation_comments:
                annotation_comment.delete()
            script.delete()

        scripts = Script.objects.all()
        for annotation_comment in AnnotationComment.objects.all():
            if not scripts.filter(uuid=annotation_comment.uuid):
                annotation_comment.delete()
        for annotation in Annotation.objects.all():
            if not scripts.filter(uuid=annotation.uuid):
                annotation.delete()


        