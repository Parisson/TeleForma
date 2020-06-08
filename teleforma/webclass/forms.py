# -*- coding: utf-8 -*-

from datetime import datetime
from django.forms import Form, ModelChoiceField, ChoiceField
from teleforma.models.core import Course, Period
from teleforma.webclass.models import get_records, WebclassSlot, WebclassRecord
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
            webclass = course.webclass.count()
            if course.webclass.count():
                rooms = []
                for webclass in course.webclass.all():
                    for slot in webclass.slots.all():
                        rooms.append(slot.room_id)

                field_name = 'course_%d' % course.id
                records = all_records.get(course.id, [])

                vocabulary = [('none', 'Aucun')]
                for record in records:
                    print(record)
                    webclass_slot = WebclassSlot.objects.get(pk=record['slot_id'])
                    label = u"%s à %s - %s" % (record['start_date'].strftime('%d/%m/%Y %H:%M'), record['end_date'].strftime('%H:%M'), webclass_slot.professor.user.last_name)
                    vocabulary.append((record['id'], label))
                self.fields[field_name] = ChoiceField(label=course.title,  choices=vocabulary, required=False)
    
    def get_records_by_course(self):
        records = get_records(period_id=self.period_id)
        by_course = {}
        for record in records:
            by_course.setdefault(record['course_id'], []).append(record)
        return by_course

    def save_records(self):
        for key, value in self.data.items():
            if key.startswith('course') and value != 'none':
                course_id = key.replace('course_', '')
                course = Course.objects.get(pk=course_id)
                record = WebclassRecord(course=course, period=self.period, record_id=value)
                record.save()
