# -*- coding: utf-8 -*-

from datetime import datetime
from django.forms import Form, ModelChoiceField, ChoiceField
from teleforma.models.core import Course, Period
from teleforma.webclass.models import get_records, WebclassSlot, WebclassRecord, BBBServer
from django.core.exceptions import ValidationError

class WebclassRecordsForm(Form):
    # period = ModelChoiceField(label='Période',
    #                         queryset=Period.objects.filter(is_open=True))

    class Meta:
        pass


    def __init__(self, *args, **kwargs):
        self.period_id = kwargs.pop('period_id')
        self.period = Period.objects.get(pk=self.period_id)
        super(WebclassRecordsForm, self).__init__(*args, **kwargs)

        courses = Course.objects.all()
        all_records = self.get_records_by_course()
        for course in courses:
            webclasses = course.webclass.filter(period=self.period).all()
            if webclasses:
                rooms = []
                for webclass in webclasses:
                    for slot in webclass.slots.all():
                        rooms.append(slot.room_id)

                field_name = 'course_%d' % course.id
                records = all_records.get(course.id, [])

                vocabulary = [('none', 'Aucun')]
                for record in records:
                    webclass_slot = WebclassSlot.objects.get(pk=record['slot'].id)
                    label = u"%s à %s - %s" % (record['start_date'].strftime('%d/%m/%Y %H:%M'), record['end_date'].strftime('%H:%M'), webclass_slot.professor.user.last_name)
                    vocabulary.append((str(record['id']) + ";" + str(record['server_id']), label))
                self.fields[field_name] = ChoiceField(label=course.title,  choices=vocabulary, required=False)

    def get_records_by_course(self):
        records = get_records(period_id=self.period_id)
        by_course = {}
        for record in records:
            if hasattr(record, 'course_id'):
                by_course.setdefault(record['course_id'], []).append(record)
        return by_course

    def save_records(self):
        for key, value in self.data.items():
            if key.startswith('course') and value != 'none':
                record_id, server_id = value.split(';')
                course_id = key.replace('course_', '')
                course = Course.objects.get(pk=course_id)
                server = BBBServer.objects.get(pk=server_id)
                record = WebclassRecord(course=course, period=self.period, record_id=record_id, bbb_server=server)
                record.save()
