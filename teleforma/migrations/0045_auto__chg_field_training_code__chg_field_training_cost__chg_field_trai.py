# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Training.code'
        db.alter_column('teleforma_training', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Training.cost'
        db.alter_column('teleforma_training', 'cost', self.gf('telemeta.models.core.FloatField')(null=True))

        # Changing field 'Training.period'
        db.alter_column('teleforma_training', 'period_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Period']))

        # Changing field 'Training.name'
        db.alter_column('teleforma_training', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.synthesis_note'
        db.alter_column('teleforma_course', 'synthesis_note', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Course.description'
        db.alter_column('teleforma_course', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.title'
        db.alter_column('teleforma_course', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.date_modified'
        db.alter_column('teleforma_course', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Course.number'
        db.alter_column('teleforma_course', 'number', self.gf('telemeta.models.core.IntegerField')(null=True))

        # Changing field 'Course.code'
        db.alter_column('teleforma_course', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.department'
        db.alter_column('teleforma_course', 'department_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Department']))

        # Changing field 'Course.magistral'
        db.alter_column('teleforma_course', 'magistral', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Course.obligation'
        db.alter_column('teleforma_course', 'obligation', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Payment.date_added'
        db.alter_column('teleforma_payment', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Payment.amount'
        db.alter_column('teleforma_payment', 'amount', self.gf('telemeta.models.core.FloatField')())

        # Changing field 'Payment.student'
        db.alter_column('teleforma_payment', 'student_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Student']))

        # Changing field 'CourseType.description'
        db.alter_column('teleforma_course_type', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'CourseType.name'
        db.alter_column('teleforma_course_type', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Professor.user'
        db.alter_column('teleforma_professor', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Document.conference'
        db.alter_column('teleforma_document', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'Document.code'
        db.alter_column('teleforma_document', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.description'
        db.alter_column('teleforma_document', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.title'
        db.alter_column('teleforma_document', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.date_modified'
        db.alter_column('teleforma_document', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Document.credits'
        db.alter_column('teleforma_document', 'credits', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.course'
        db.alter_column('teleforma_document', 'course_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Document.file'
        db.alter_column('teleforma_document', 'filename', self.gf('telemeta.models.core.FileField')(max_length=100, db_column='filename'))

        # Changing field 'Document.date_added'
        db.alter_column('teleforma_document', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Document.is_published'
        db.alter_column('teleforma_document', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Document.type'
        db.alter_column('teleforma_document', 'type_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.DocumentType']))

        # Changing field 'Document.is_annal'
        db.alter_column('teleforma_document', 'is_annal', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'StreamingServer.description'
        db.alter_column('teleforma_streaming_server', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'StreamingServer.source_password'
        db.alter_column('teleforma_streaming_server', 'source_password', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'StreamingServer.host'
        db.alter_column('teleforma_streaming_server', 'host', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'StreamingServer.admin_password'
        db.alter_column('teleforma_streaming_server', 'admin_password', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'StreamingServer.type'
        db.alter_column('teleforma_streaming_server', 'type', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'StreamingServer.port'
        db.alter_column('teleforma_streaming_server', 'port', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'LiveStream.conference'
        db.alter_column('teleforma_live_stream', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'LiveStream.streaming'
        db.alter_column('teleforma_live_stream', 'streaming', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'LiveStream.stream_type'
        db.alter_column('teleforma_live_stream', 'stream_type', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'LiveStream.server'
        db.alter_column('teleforma_live_stream', 'server_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.StreamingServer']))

        # Changing field 'Student.training'
        db.alter_column('teleforma_student', 'training_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Training']))

        # Changing field 'Student.oral_speciality'
        db.alter_column('teleforma_student', 'oral_speciality_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.platform_only'
        db.alter_column('teleforma_student', 'platform_only', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Student.oral_2'
        db.alter_column('teleforma_student', 'oral_2_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.oral_1'
        db.alter_column('teleforma_student', 'oral_1_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.iej'
        db.alter_column('teleforma_student', 'iej_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.IEJ'], null=True))

        # Changing field 'Student.user'
        db.alter_column('teleforma_student', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Student.options'
        db.alter_column('teleforma_student', 'options_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.written_speciality'
        db.alter_column('teleforma_student', 'written_speciality_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.procedure'
        db.alter_column('teleforma_student', 'procedure_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'IEJ.description'
        db.alter_column('teleforma_iej', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'IEJ.name'
        db.alter_column('teleforma_iej', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentType.description'
        db.alter_column('teleforma_document_type', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentType.name'
        db.alter_column('teleforma_document_type', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentType.number'
        db.alter_column('teleforma_document_type', 'number', self.gf('telemeta.models.core.IntegerField')(null=True))

        # Changing field 'Profile.city'
        db.alter_column('teleforma_profiles', 'city', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.language'
        db.alter_column('teleforma_profiles', 'language', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.expiration_date'
        db.alter_column('teleforma_profiles', 'expiration_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'Profile.init_password'
        db.alter_column('teleforma_profiles', 'init_password', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Profile.telephone'
        db.alter_column('teleforma_profiles', 'telephone', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.postal_code'
        db.alter_column('teleforma_profiles', 'postal_code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.user'
        db.alter_column('teleforma_profiles', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Profile.country'
        db.alter_column('teleforma_profiles', 'country', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.address'
        db.alter_column('teleforma_profiles', 'address', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Period.description'
        db.alter_column('teleforma_period', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Period.name'
        db.alter_column('teleforma_period', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Organization.description'
        db.alter_column('teleforma_organization', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Organization.name'
        db.alter_column('teleforma_organization', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))
        # Adding field 'Media.item'
        db.add_column('teleforma_media', 'item',
                      self.gf('telemeta.models.core.ForeignKey')(default=None, related_name='media', null=True, blank=True, to=orm['telemeta.MediaItem']),
                      keep_default=False)

        # Adding field 'Media.type'
        db.add_column('teleforma_media', 'type',
                      self.gf('telemeta.models.core.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)

        # Removing M2M table for field items on 'Media'
        db.delete_table('teleforma_media_items')


        # Changing field 'Media.conference'
        db.alter_column('teleforma_media', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'Media.code'
        db.alter_column('teleforma_media', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.description'
        db.alter_column('teleforma_media', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.title'
        db.alter_column('teleforma_media', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.date_modified'
        db.alter_column('teleforma_media', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Media.course_type'
        db.alter_column('teleforma_media', 'course_type_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.CourseType']))

        # Changing field 'Media.course'
        db.alter_column('teleforma_media', 'course_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Media.date_added'
        db.alter_column('teleforma_media', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Media.credits'
        db.alter_column('teleforma_media', 'credits', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.is_published'
        db.alter_column('teleforma_media', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Conference.public_id'
        db.alter_column('teleforma_conference', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Conference.room'
        db.alter_column('teleforma_conference', 'room_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Room']))

        # Changing field 'Conference.course'
        db.alter_column('teleforma_conference', 'course_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Conference.professor'
        db.alter_column('teleforma_conference', 'professor_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Professor'], null=True))

        # Changing field 'Conference.course_type'
        db.alter_column('teleforma_conference', 'course_type_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.CourseType']))

        # Changing field 'Conference.session'
        db.alter_column('teleforma_conference', 'session', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'Conference.date_begin'
        db.alter_column('teleforma_conference', 'date_begin', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'Conference.date_end'
        db.alter_column('teleforma_conference', 'date_end', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'Department.organization'
        db.alter_column('teleforma_department', 'organization_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Department.domain'
        db.alter_column('teleforma_department', 'domain', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Department.description'
        db.alter_column('teleforma_department', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Department.name'
        db.alter_column('teleforma_department', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Room.organization'
        db.alter_column('teleforma_room', 'organization_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Room.description'
        db.alter_column('teleforma_room', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Room.name'
        db.alter_column('teleforma_room', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))
    def backwards(self, orm):

        # Changing field 'Training.code'
        db.alter_column('teleforma_training', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Training.cost'
        db.alter_column('teleforma_training', 'cost', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Training.period'
        db.alter_column('teleforma_training', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Period']))

        # Changing field 'Training.name'
        db.alter_column('teleforma_training', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.synthesis_note'
        db.alter_column('teleforma_course', 'synthesis_note', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Course.description'
        db.alter_column('teleforma_course', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.title'
        db.alter_column('teleforma_course', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.date_modified'
        db.alter_column('teleforma_course', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=1))

        # Changing field 'Course.number'
        db.alter_column('teleforma_course', 'number', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Course.code'
        db.alter_column('teleforma_course', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.department'
        db.alter_column('teleforma_course', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Department']))

        # Changing field 'Course.magistral'
        db.alter_column('teleforma_course', 'magistral', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Course.obligation'
        db.alter_column('teleforma_course', 'obligation', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Payment.date_added'
        db.alter_column('teleforma_payment', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=1))

        # Changing field 'Payment.amount'
        db.alter_column('teleforma_payment', 'amount', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Payment.student'
        db.alter_column('teleforma_payment', 'student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Student']))

        # Changing field 'CourseType.description'
        db.alter_column('teleforma_course_type', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'CourseType.name'
        db.alter_column('teleforma_course_type', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Professor.user'
        db.alter_column('teleforma_professor', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Document.conference'
        db.alter_column('teleforma_document', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Conference'], on_delete=models.SET_NULL))

        # Changing field 'Document.code'
        db.alter_column('teleforma_document', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.description'
        db.alter_column('teleforma_document', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.title'
        db.alter_column('teleforma_document', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.date_modified'
        db.alter_column('teleforma_document', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=1))

        # Changing field 'Document.credits'
        db.alter_column('teleforma_document', 'credits', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.course'
        db.alter_column('teleforma_document', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Document.file'
        db.alter_column('teleforma_document', 'filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, db_column='filename'))

        # Changing field 'Document.date_added'
        db.alter_column('teleforma_document', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=1))

        # Changing field 'Document.is_published'
        db.alter_column('teleforma_document', 'is_published', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Document.type'
        db.alter_column('teleforma_document', 'type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.DocumentType']))

        # Changing field 'Document.is_annal'
        db.alter_column('teleforma_document', 'is_annal', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'StreamingServer.description'
        db.alter_column('teleforma_streaming_server', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'StreamingServer.source_password'
        db.alter_column('teleforma_streaming_server', 'source_password', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'StreamingServer.host'
        db.alter_column('teleforma_streaming_server', 'host', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'StreamingServer.admin_password'
        db.alter_column('teleforma_streaming_server', 'admin_password', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'StreamingServer.type'
        db.alter_column('teleforma_streaming_server', 'type', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'StreamingServer.port'
        db.alter_column('teleforma_streaming_server', 'port', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'LiveStream.conference'
        db.alter_column('teleforma_live_stream', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Conference'], on_delete=models.SET_NULL))

        # Changing field 'LiveStream.streaming'
        db.alter_column('teleforma_live_stream', 'streaming', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LiveStream.stream_type'
        db.alter_column('teleforma_live_stream', 'stream_type', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'LiveStream.server'
        db.alter_column('teleforma_live_stream', 'server_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.StreamingServer']))

        # Changing field 'Student.training'
        db.alter_column('teleforma_student', 'training_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Training']))

        # Changing field 'Student.oral_speciality'
        db.alter_column('teleforma_student', 'oral_speciality_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.platform_only'
        db.alter_column('teleforma_student', 'platform_only', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Student.oral_2'
        db.alter_column('teleforma_student', 'oral_2_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.oral_1'
        db.alter_column('teleforma_student', 'oral_1_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.iej'
        db.alter_column('teleforma_student', 'iej_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.IEJ'], on_delete=models.SET_NULL))

        # Changing field 'Student.user'
        db.alter_column('teleforma_student', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Student.options'
        db.alter_column('teleforma_student', 'options_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.written_speciality'
        db.alter_column('teleforma_student', 'written_speciality_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.procedure'
        db.alter_column('teleforma_student', 'procedure_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'IEJ.description'
        db.alter_column('teleforma_iej', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'IEJ.name'
        db.alter_column('teleforma_iej', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentType.description'
        db.alter_column('teleforma_document_type', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentType.name'
        db.alter_column('teleforma_document_type', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentType.number'
        db.alter_column('teleforma_document_type', 'number', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Profile.city'
        db.alter_column('teleforma_profiles', 'city', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.language'
        db.alter_column('teleforma_profiles', 'language', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.expiration_date'
        db.alter_column('teleforma_profiles', 'expiration_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Profile.init_password'
        db.alter_column('teleforma_profiles', 'init_password', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Profile.telephone'
        db.alter_column('teleforma_profiles', 'telephone', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.postal_code'
        db.alter_column('teleforma_profiles', 'postal_code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.user'
        db.alter_column('teleforma_profiles', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Profile.country'
        db.alter_column('teleforma_profiles', 'country', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.address'
        db.alter_column('teleforma_profiles', 'address', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Period.description'
        db.alter_column('teleforma_period', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Period.name'
        db.alter_column('teleforma_period', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Organization.description'
        db.alter_column('teleforma_organization', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Organization.name'
        db.alter_column('teleforma_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))
        # Deleting field 'Media.item'
        db.delete_column('teleforma_media', 'item_id')

        # Deleting field 'Media.type'
        db.delete_column('teleforma_media', 'type')

        # Adding M2M table for field items on 'Media'
        db.create_table('teleforma_media_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('media', models.ForeignKey(orm['teleforma.media'], null=False)),
            ('mediaitem', models.ForeignKey(orm['telemeta.mediaitem'], null=False))
        ))
        db.create_unique('teleforma_media_items', ['media_id', 'mediaitem_id'])


        # Changing field 'Media.conference'
        db.alter_column('teleforma_media', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Conference'], on_delete=models.SET_NULL))

        # Changing field 'Media.code'
        db.alter_column('teleforma_media', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.description'
        db.alter_column('teleforma_media', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.title'
        db.alter_column('teleforma_media', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.date_modified'
        db.alter_column('teleforma_media', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=1))

        # Changing field 'Media.course_type'
        db.alter_column('teleforma_media', 'course_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.CourseType']))

        # Changing field 'Media.course'
        db.alter_column('teleforma_media', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Media.date_added'
        db.alter_column('teleforma_media', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=1))

        # Changing field 'Media.credits'
        db.alter_column('teleforma_media', 'credits', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.is_published'
        db.alter_column('teleforma_media', 'is_published', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Conference.public_id'
        db.alter_column('teleforma_conference', 'public_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Conference.room'
        db.alter_column('teleforma_conference', 'room_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Room']))

        # Changing field 'Conference.course'
        db.alter_column('teleforma_conference', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Conference.professor'
        db.alter_column('teleforma_conference', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Professor'], on_delete=models.SET_NULL))

        # Changing field 'Conference.course_type'
        db.alter_column('teleforma_conference', 'course_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.CourseType']))

        # Changing field 'Conference.session'
        db.alter_column('teleforma_conference', 'session', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Conference.date_begin'
        db.alter_column('teleforma_conference', 'date_begin', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Conference.date_end'
        db.alter_column('teleforma_conference', 'date_end', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Department.organization'
        db.alter_column('teleforma_department', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Department.domain'
        db.alter_column('teleforma_department', 'domain', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Department.description'
        db.alter_column('teleforma_department', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Department.name'
        db.alter_column('teleforma_department', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Room.organization'
        db.alter_column('teleforma_room', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Room.description'
        db.alter_column('teleforma_room', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Room.name'
        db.alter_column('teleforma_room', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rendered_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notes.Topic']"})
        },
        'notes.topic': {
            'Meta': {'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.conference': {
            'Meta': {'ordering': "['-date_begin']", 'object_name': 'Conference'},
            'comment': ('teleforma.models.ShortTextField', [], {'max_length': '255', 'blank': 'True'}),
            'course': ('telemeta.models.core.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('telemeta.models.core.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.CourseType']"}),
            'date_begin': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_end': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('telemeta.models.core.ForeignKey', [], {'related_name': "'conference'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.Professor']", 'blank': 'True', 'null': 'True'}),
            'public_id': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'room': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'conference'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('telemeta.models.core.CharField', [], {'default': "'1'", 'max_length': '16', 'blank': 'True'})
        },
        'teleforma.course': {
            'Meta': {'ordering': "['number']", 'object_name': 'Course'},
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'date_modified': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'department': ('telemeta.models.core.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'number': ('telemeta.models.core.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'obligation': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'synthesis_note': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.coursetype': {
            'Meta': {'object_name': 'CourseType', 'db_table': "'teleforma_course_type'"},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'domain': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'organization': ('telemeta.models.core.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'conference': ('telemeta.models.core.ForeignKey', [], {'related_name': "'document'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.Conference']", 'blank': 'True', 'null': 'True'}),
            'course': ('telemeta.models.core.ForeignKey', [], {'related_name': "'document'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'date_added': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '100', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_annal': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'is_published': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'type': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'document'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.DocumentType']"})
        },
        'teleforma.documenttype': {
            'Meta': {'ordering': "['number']", 'object_name': 'DocumentType', 'db_table': "'teleforma_document_type'"},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'number': ('telemeta.models.core.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'teleforma.iej': {
            'Meta': {'ordering': "['name']", 'object_name': 'IEJ'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.livestream': {
            'Meta': {'object_name': 'LiveStream', 'db_table': "'teleforma_live_stream'"},
            'conference': ('telemeta.models.core.ForeignKey', [], {'related_name': "'livestream'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.Conference']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('telemeta.models.core.ForeignKey', [], {'related_name': "'livestream'", 'to': "orm['teleforma.StreamingServer']"}),
            'stream_type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'streaming': ('telemeta.models.core.BooleanField', [], {'default': 'False'})
        },
        'teleforma.media': {
            'Meta': {'ordering': "['-date_modified']", 'object_name': 'Media'},
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'conference': ('telemeta.models.core.ForeignKey', [], {'related_name': "'media'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.Conference']", 'blank': 'True', 'null': 'True'}),
            'course': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'media'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"}),
            'course_type': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'media'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'date_added': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'item': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'media'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.payment': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Payment'},
            'amount': ('telemeta.models.core.FloatField', [], {'default': '0', 'blank': 'True'}),
            'date_added': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('telemeta.models.core.ForeignKey', [], {'related_name': "'payment'", 'to': "orm['teleforma.Student']"})
        },
        'teleforma.period': {
            'Meta': {'object_name': 'Period'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.professor': {
            'Meta': {'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'teleforma_profiles'"},
            'address': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'city': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'country': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'expiration_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_password': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'postal_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'telephone': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'organization': ('telemeta.models.core.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.streamingserver': {
            'Meta': {'object_name': 'StreamingServer', 'db_table': "'teleforma_streaming_server'"},
            'admin_password': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'host': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'source_password': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'})
        },
        'teleforma.student': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'Student'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('telemeta.models.core.ForeignKey', [], {'related_name': "'student'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.IEJ']", 'blank': 'True', 'null': 'True'}),
            'options': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'options'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_1': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'oral_1'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_2': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'oral_2'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_speciality': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'oral_speciality'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"}),
            'period': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'procedure': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'procedure'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"}),
            'training': ('telemeta.models.core.ForeignKey', [], {'related_name': "'student'", 'to': "orm['teleforma.Training']"}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'student'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'written_speciality': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'written_speciality'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Course']"})
        },
        'teleforma.training': {
            'Meta': {'object_name': 'Training'},
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'cost': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_magistral'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_obligation'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_options'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_1': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_1'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_2': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_2'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_speciality': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_speciality'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'period': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'training'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Period']"}),
            'procedure': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_procedure'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'synthesis_note': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_synthesis_note'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'written_speciality': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_written_speciality'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"})
        },
        'telemeta.acquisitionmode': {
            'Meta': {'ordering': "['value']", 'object_name': 'AcquisitionMode', 'db_table': "'acquisition_modes'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.adconversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'AdConversion', 'db_table': "'ad_conversions'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.ethnicgroup': {
            'Meta': {'ordering': "['value']", 'object_name': 'EthnicGroup', 'db_table': "'ethnic_groups'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.genericstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'GenericStyle', 'db_table': "'generic_styles'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language', 'db_table': "'languages'"},
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'part1': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'part2B': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'part2T': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'scope': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'type': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
        },
        'telemeta.legalright': {
            'Meta': {'ordering': "['value']", 'object_name': 'LegalRight', 'db_table': "'legal_rights'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location', 'db_table': "'locations'"},
            'complete_type': ('telemeta.models.core.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['telemeta.LocationType']"}),
            'current_location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'past_names'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Location']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'latitude': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('telemeta.models.core.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'type': ('telemeta.models.core.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'telemeta.locationtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocationType', 'db_table': "'location_types'"},
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'max_length': '150'})
        },
        'telemeta.mediacollection': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCollection', 'db_table': "'media_collections'"},
            'a_informer_07_03': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'acquisition_mode': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AcquisitionMode']"}),
            'ad_conversion': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AdConversion']"}),
            'alt_ids': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'booklet_author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'booklet_description': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'cnrs_contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_is_creator': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'conservation_site': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'creator': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'doctype_code': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'items_done': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'legal_rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.LegalRight']"}),
            'metadata_author': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataAuthor']"}),
            'metadata_writer': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataWriter']"}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'physical_format': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'physical_items_num': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publisher': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Publisher']"}),
            'publisher_collection': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublisherCollection']"}),
            'publisher_serial': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'publishing_status': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublishingStatus']"}),
            'recorded_from_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recording_context': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.RecordingContext']"}),
            'reference': ('telemeta.models.core.CharField', [], {'default': 'None', 'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'max_length': '250'}),
            'travail': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'year_published': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telemeta.mediaitem': {
            'Meta': {'object_name': 'MediaItem', 'db_table': "'media_items'"},
            'alt_title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'contributor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'copied_from_item': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'copies'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'creator_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'depositor': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitalist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitization_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '255', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
            'location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'organization': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Organization']", 'null': 'True', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publishing_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recordist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'rights': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Rights']", 'null': 'True', 'blank': 'True'}),
            'scientist': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'summary': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'topic': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Topic']", 'null': 'True', 'blank': 'True'}),
            'track': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'vernacular_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.VernacularStyle']"})
        },
        'telemeta.metadataauthor': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataAuthor', 'db_table': "'metadata_authors'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadatawriter': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataWriter', 'db_table': "'metadata_writers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.organization': {
            'Meta': {'ordering': "['value']", 'object_name': 'Organization', 'db_table': "'organization'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.physicalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'PhysicalFormat', 'db_table': "'physical_formats'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publisher': {
            'Meta': {'ordering': "['value']", 'object_name': 'Publisher', 'db_table': "'publishers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publishercollection': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublisherCollection', 'db_table': "'publisher_collections'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('telemeta.models.core.ForeignKey', [], {'related_name': "'publisher_collections'", 'to': "orm['telemeta.Publisher']"}),
            'value': ('telemeta.models.core.CharField', [], {'max_length': '250'})
        },
        'telemeta.publishingstatus': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublishingStatus', 'db_table': "'publishing_status'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.recordingcontext': {
            'Meta': {'ordering': "['value']", 'object_name': 'RecordingContext', 'db_table': "'recording_contexts'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.rights': {
            'Meta': {'ordering': "['value']", 'object_name': 'Rights', 'db_table': "'rights'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.topic': {
            'Meta': {'ordering': "['value']", 'object_name': 'Topic', 'db_table': "'topic'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['teleforma']