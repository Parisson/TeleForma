# -*- coding: utf-8 -*-

from datetime import datetime
from django.forms import Form, ModelChoiceField, ChoiceField
from teleforma.models.core import Course, Period
from teleforma.webclass.models import get_records, WebclassSlot, WebclassRecord, BBBServer
from django.core.exceptions import ValidationError

class WebclassRecordsForm(Form):

    def __init__(self, *args, **kwargs):
        # for each course, we create a field whcih includes a list of bbb course from the same course id and same period id
        self.period_id = kwargs.pop('period_id')
        self.period = Period.objects.get(pk=self.period_id)
        super(WebclassRecordsForm, self).__init__(*args, **kwargs)

        courses = Course.objects.all()
        all_records = self.get_records_by_course()
        
        for course in courses:
            # get list of webclass
            webclasses = course.webclass.filter(period=self.period).all()
            if webclasses:
                # build a rooms id list
                rooms = []
                for webclass in webclasses:
                    for slot in webclass.slots.all():
                        rooms.append(slot.room_id)

                field_name = 'course_%d' % course.id
                records = all_records.get(course.id, [])
                print(records)

                vocabulary = [('none', 'Aucun')]
                # for each bbb record for the current course, add an option to the field
                
                for record in records:
                    webclass_slot = WebclassSlot.objects.get(pk=record['slot'].id)
                    label = u"%s à %s - %s" % (record['start_date'].strftime('%d/%m/%Y %H:%M'), record['end_date'].strftime('%H:%M'), webclass_slot.professor.user.last_name)
                    vocabulary.append((str(record['id']) + ";" + str(record['server_id']), label))
                self.fields[field_name] = ChoiceField(label=course.title,  choices=vocabulary, required=False)

    def get_records_by_course(self):
        """ 
        Get all records, in a dict with course_id as key 
        """
        records = get_records(period_id=self.period_id)
        by_course = {}
        for record in records:
            if record.get('course_id'):
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
