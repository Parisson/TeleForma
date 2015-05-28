# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Training.code'
        db.alter_column('teleforma_training', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Training.cost'
        db.alter_column('teleforma_training', 'cost', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Training.period'
        db.alter_column('teleforma_training', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Period']))

        # Changing field 'Training.name'
        db.alter_column('teleforma_training', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Organization.description'
        db.alter_column('teleforma_organization', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Organization.name'
        db.alter_column('teleforma_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Period.description'
        db.alter_column('teleforma_period', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Period.name'
        db.alter_column('teleforma_period', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Room.organization'
        db.alter_column('teleforma_room', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Room.description'
        db.alter_column('teleforma_room', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Room.name'
        db.alter_column('teleforma_room', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.conference'
        db.alter_column('teleforma_media', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Conference']))

        # Changing field 'Media.code'
        db.alter_column('teleforma_media', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.description'
        db.alter_column('teleforma_media', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.title'
        db.alter_column('teleforma_media', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.date_modified'
        db.alter_column('teleforma_media', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Media.period'
        db.alter_column('teleforma_media', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Media.course_type'
        db.alter_column('teleforma_media', 'course_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.CourseType']))

        # Changing field 'Media.course'
        db.alter_column('teleforma_media', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Media.item'
        db.alter_column('teleforma_media', 'item_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telemeta.MediaItem']))

        # Changing field 'Media.date_added'
        db.alter_column('teleforma_media', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Media.credits'
        db.alter_column('teleforma_media', 'credits', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.type'
        db.alter_column('teleforma_media', 'type', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'Media.mime_type'
        db.alter_column('teleforma_media', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.is_published'
        db.alter_column('teleforma_media', 'is_published', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Course.code'
        db.alter_column('teleforma_course', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.description'
        db.alter_column('teleforma_course', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.date_modified'
        db.alter_column('teleforma_course', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Course.title_tweeter'
        db.alter_column('teleforma_course', 'title_tweeter', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.title'
        db.alter_column('teleforma_course', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.number'
        db.alter_column('teleforma_course', 'number', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Course.synthesis_note'
        db.alter_column('teleforma_course', 'synthesis_note', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Course.department'
        db.alter_column('teleforma_course', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Department']))

        # Changing field 'Course.magistral'
        db.alter_column('teleforma_course', 'magistral', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Course.obligation'
        db.alter_column('teleforma_course', 'obligation', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Document.conference'
        db.alter_column('teleforma_document', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Conference']))

        # Changing field 'Document.is_published'
        db.alter_column('teleforma_document', 'is_published', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Document.code'
        db.alter_column('teleforma_document', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.description'
        db.alter_column('teleforma_document', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.date_modified'
        db.alter_column('teleforma_document', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Document.title'
        db.alter_column('teleforma_document', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.period'
        db.alter_column('teleforma_document', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Document.annal_year'
        db.alter_column('teleforma_document', 'annal_year', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Document.credits'
        db.alter_column('teleforma_document', 'credits', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.iej'
        db.alter_column('teleforma_document', 'iej_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.IEJ']))

        # Changing field 'Document.session'
        db.alter_column('teleforma_document', 'session', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Document.file'
        db.alter_column('teleforma_document', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'Document.date_added'
        db.alter_column('teleforma_document', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Document.course'
        db.alter_column('teleforma_document', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Document.type'
        db.alter_column('teleforma_document', 'type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.DocumentType']))

        # Changing field 'Document.mime_type'
        db.alter_column('teleforma_document', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.is_annal'
        db.alter_column('teleforma_document', 'is_annal', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'IEJ.description'
        db.alter_column('teleforma_iej', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'IEJ.name'
        db.alter_column('teleforma_iej', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

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

        # Changing field 'DocumentSimple.code'
        db.alter_column('teleforma_document_simple', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentSimple.description'
        db.alter_column('teleforma_document_simple', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentSimple.title'
        db.alter_column('teleforma_document_simple', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentSimple.date_modified'
        db.alter_column('teleforma_document_simple', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'DocumentSimple.period'
        db.alter_column('teleforma_document_simple', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'DocumentSimple.credits'
        db.alter_column('teleforma_document_simple', 'credits', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentSimple.file'
        db.alter_column('teleforma_document_simple', 'filename', self.gf('telemeta.models.fields.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'DocumentSimple.date_added'
        db.alter_column('teleforma_document_simple', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'DocumentSimple.mime_type'
        db.alter_column('teleforma_document_simple', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentSimple.is_published'
        db.alter_column('teleforma_document_simple', 'is_published', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Student.application_fees'
        db.alter_column('teleforma_student', 'application_fees', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Student.subscription_fees'
        db.alter_column('teleforma_student', 'subscription_fees', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Student.is_subscribed'
        db.alter_column('teleforma_student', 'is_subscribed', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Student.oral_speciality'
        db.alter_column('teleforma_student', 'oral_speciality_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.period'
        db.alter_column('teleforma_student', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Student.platform_only'
        db.alter_column('teleforma_student', 'platform_only', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Student.oral_2'
        db.alter_column('teleforma_student', 'oral_2_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.oral_1'
        db.alter_column('teleforma_student', 'oral_1_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.iej'
        db.alter_column('teleforma_student', 'iej_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.IEJ']))

        # Changing field 'Student.written_speciality'
        db.alter_column('teleforma_student', 'written_speciality_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.user'
        db.alter_column('teleforma_student', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Student.confirmation_sent'
        db.alter_column('teleforma_student', 'confirmation_sent', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Student.date_subscribed'
        db.alter_column('teleforma_student', 'date_subscribed', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Student.procedure'
        db.alter_column('teleforma_student', 'procedure_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.options'
        db.alter_column('teleforma_student', 'options_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'AEStudent.user'
        db.alter_column('teleforma_ae_student', 'user_id', self.gf('telemeta.models.fields.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'AEStudent.platform_only'
        db.alter_column('teleforma_ae_student', 'platform_only', self.gf('telemeta.models.fields.BooleanField')())

        # Changing field 'DocumentType.description'
        db.alter_column('teleforma_document_type', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentType.name'
        db.alter_column('teleforma_document_type', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'DocumentType.number'
        db.alter_column('teleforma_document_type', 'number', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Profile.city'
        db.alter_column('teleforma_profiles', 'city', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.expiration_date'
        db.alter_column('teleforma_profiles', 'expiration_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Profile.wifi_pass'
        db.alter_column('teleforma_profiles', 'wifi_pass', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.language'
        db.alter_column('teleforma_profiles', 'language', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.country'
        db.alter_column('teleforma_profiles', 'country', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.wifi_login'
        db.alter_column('teleforma_profiles', 'wifi_login', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.telephone'
        db.alter_column('teleforma_profiles', 'telephone', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.postal_code'
        db.alter_column('teleforma_profiles', 'postal_code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Profile.user'
        db.alter_column('teleforma_profiles', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Profile.init_password'
        db.alter_column('teleforma_profiles', 'init_password', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Profile.address'
        db.alter_column('teleforma_profiles', 'address', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Department.domain'
        db.alter_column('teleforma_department', 'domain', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Department.description'
        db.alter_column('teleforma_department', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Department.default_period'
        db.alter_column('teleforma_department', 'default_period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Department.organization'
        db.alter_column('teleforma_department', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Department.name'
        db.alter_column('teleforma_department', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'CourseType.description'
        db.alter_column('teleforma_course_type', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'CourseType.name'
        db.alter_column('teleforma_course_type', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Professor.department'
        db.alter_column('teleforma_professor', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Department']))

        # Changing field 'Professor.user'
        db.alter_column('teleforma_professor', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Conference.public_id'
        db.alter_column('teleforma_conference', 'public_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Conference.room'
        db.alter_column('teleforma_conference', 'room_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Room']))

        # Changing field 'Conference.course'
        db.alter_column('teleforma_conference', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Conference.professor'
        db.alter_column('teleforma_conference', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Professor']))

        # Changing field 'Conference.period'
        db.alter_column('teleforma_conference', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Conference.course_type'
        db.alter_column('teleforma_conference', 'course_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.CourseType']))

        # Changing field 'Conference.session'
        db.alter_column('teleforma_conference', 'session', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Conference.department'
        db.alter_column('teleforma_conference', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Department']))

        # Changing field 'Conference.date_begin'
        db.alter_column('teleforma_conference', 'date_begin', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Conference.date_end'
        db.alter_column('teleforma_conference', 'date_end', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'LiveStream.conference'
        db.alter_column('teleforma_live_stream', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Conference']))

        # Changing field 'LiveStream.streaming'
        db.alter_column('teleforma_live_stream', 'streaming', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LiveStream.stream_type'
        db.alter_column('teleforma_live_stream', 'stream_type', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'LiveStream.server'
        db.alter_column('teleforma_live_stream', 'server_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.StreamingServer']))

    def backwards(self, orm):

        # Changing field 'Training.code'
        db.alter_column('teleforma_training', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Training.cost'
        db.alter_column('teleforma_training', 'cost', self.gf('telemeta.models.core.FloatField')(null=True))

        # Changing field 'Training.period'
        db.alter_column('teleforma_training', 'period_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Period']))

        # Changing field 'Training.name'
        db.alter_column('teleforma_training', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Organization.description'
        db.alter_column('teleforma_organization', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Organization.name'
        db.alter_column('teleforma_organization', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Period.description'
        db.alter_column('teleforma_period', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Period.name'
        db.alter_column('teleforma_period', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Room.organization'
        db.alter_column('teleforma_room', 'organization_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Room.description'
        db.alter_column('teleforma_room', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Room.name'
        db.alter_column('teleforma_room', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

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

        # Changing field 'Media.period'
        db.alter_column('teleforma_media', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Media.course_type'
        db.alter_column('teleforma_media', 'course_type_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.CourseType']))

        # Changing field 'Media.course'
        db.alter_column('teleforma_media', 'course_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Media.item'
        db.alter_column('teleforma_media', 'item_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['telemeta.MediaItem']))

        # Changing field 'Media.date_added'
        db.alter_column('teleforma_media', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Media.credits'
        db.alter_column('teleforma_media', 'credits', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.type'
        db.alter_column('teleforma_media', 'type', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'Media.mime_type'
        db.alter_column('teleforma_media', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.is_published'
        db.alter_column('teleforma_media', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Course.code'
        db.alter_column('teleforma_course', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.description'
        db.alter_column('teleforma_course', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.date_modified'
        db.alter_column('teleforma_course', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Course.title_tweeter'
        db.alter_column('teleforma_course', 'title_tweeter', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.title'
        db.alter_column('teleforma_course', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.number'
        db.alter_column('teleforma_course', 'number', self.gf('telemeta.models.core.IntegerField')(null=True))

        # Changing field 'Course.synthesis_note'
        db.alter_column('teleforma_course', 'synthesis_note', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Course.department'
        db.alter_column('teleforma_course', 'department_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Department']))

        # Changing field 'Course.magistral'
        db.alter_column('teleforma_course', 'magistral', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Course.obligation'
        db.alter_column('teleforma_course', 'obligation', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Document.conference'
        db.alter_column('teleforma_document', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'Document.is_published'
        db.alter_column('teleforma_document', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Document.code'
        db.alter_column('teleforma_document', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.description'
        db.alter_column('teleforma_document', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.date_modified'
        db.alter_column('teleforma_document', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Document.title'
        db.alter_column('teleforma_document', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.period'
        db.alter_column('teleforma_document', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Document.annal_year'
        db.alter_column('teleforma_document', 'annal_year', self.gf('telemeta.models.core.IntegerField')(null=True))

        # Changing field 'Document.credits'
        db.alter_column('teleforma_document', 'credits', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.iej'
        db.alter_column('teleforma_document', 'iej_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.IEJ'], null=True))

        # Changing field 'Document.session'
        db.alter_column('teleforma_document', 'session', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'Document.file'
        db.alter_column('teleforma_document', 'filename', self.gf('telemeta.models.core.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'Document.date_added'
        db.alter_column('teleforma_document', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Document.course'
        db.alter_column('teleforma_document', 'course_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Document.type'
        db.alter_column('teleforma_document', 'type_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.DocumentType']))

        # Changing field 'Document.mime_type'
        db.alter_column('teleforma_document', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.is_annal'
        db.alter_column('teleforma_document', 'is_annal', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'IEJ.description'
        db.alter_column('teleforma_iej', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'IEJ.name'
        db.alter_column('teleforma_iej', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

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

        # Changing field 'DocumentSimple.code'
        db.alter_column('teleforma_document_simple', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentSimple.description'
        db.alter_column('teleforma_document_simple', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentSimple.title'
        db.alter_column('teleforma_document_simple', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentSimple.date_modified'
        db.alter_column('teleforma_document_simple', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'DocumentSimple.period'
        db.alter_column('teleforma_document_simple', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'DocumentSimple.credits'
        db.alter_column('teleforma_document_simple', 'credits', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentSimple.file'
        db.alter_column('teleforma_document_simple', 'filename', self.gf('telemeta.models.core.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'DocumentSimple.date_added'
        db.alter_column('teleforma_document_simple', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'DocumentSimple.mime_type'
        db.alter_column('teleforma_document_simple', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentSimple.is_published'
        db.alter_column('teleforma_document_simple', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Student.application_fees'
        db.alter_column('teleforma_student', 'application_fees', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Student.subscription_fees'
        db.alter_column('teleforma_student', 'subscription_fees', self.gf('telemeta.models.core.FloatField')())

        # Changing field 'Student.is_subscribed'
        db.alter_column('teleforma_student', 'is_subscribed', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Student.oral_speciality'
        db.alter_column('teleforma_student', 'oral_speciality_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.period'
        db.alter_column('teleforma_student', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Student.platform_only'
        db.alter_column('teleforma_student', 'platform_only', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Student.oral_2'
        db.alter_column('teleforma_student', 'oral_2_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.oral_1'
        db.alter_column('teleforma_student', 'oral_1_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.iej'
        db.alter_column('teleforma_student', 'iej_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.IEJ'], null=True))

        # Changing field 'Student.written_speciality'
        db.alter_column('teleforma_student', 'written_speciality_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.user'
        db.alter_column('teleforma_student', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Student.confirmation_sent'
        db.alter_column('teleforma_student', 'confirmation_sent', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Student.date_subscribed'
        db.alter_column('teleforma_student', 'date_subscribed', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'Student.procedure'
        db.alter_column('teleforma_student', 'procedure_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.options'
        db.alter_column('teleforma_student', 'options_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'AEStudent.user'
        db.alter_column('teleforma_ae_student', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'AEStudent.platform_only'
        db.alter_column('teleforma_ae_student', 'platform_only', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'DocumentType.description'
        db.alter_column('teleforma_document_type', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentType.name'
        db.alter_column('teleforma_document_type', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'DocumentType.number'
        db.alter_column('teleforma_document_type', 'number', self.gf('telemeta.models.core.IntegerField')(null=True))

        # Changing field 'Profile.city'
        db.alter_column('teleforma_profiles', 'city', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.expiration_date'
        db.alter_column('teleforma_profiles', 'expiration_date', self.gf('telemeta.models.core.DateField')(null=True))

        # Changing field 'Profile.wifi_pass'
        db.alter_column('teleforma_profiles', 'wifi_pass', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.language'
        db.alter_column('teleforma_profiles', 'language', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.country'
        db.alter_column('teleforma_profiles', 'country', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.wifi_login'
        db.alter_column('teleforma_profiles', 'wifi_login', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.telephone'
        db.alter_column('teleforma_profiles', 'telephone', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.postal_code'
        db.alter_column('teleforma_profiles', 'postal_code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Profile.user'
        db.alter_column('teleforma_profiles', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Profile.init_password'
        db.alter_column('teleforma_profiles', 'init_password', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Profile.address'
        db.alter_column('teleforma_profiles', 'address', self.gf('telemeta.models.core.TextField')())

        # Changing field 'Department.domain'
        db.alter_column('teleforma_department', 'domain', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Department.description'
        db.alter_column('teleforma_department', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Department.default_period'
        db.alter_column('teleforma_department', 'default_period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Department.organization'
        db.alter_column('teleforma_department', 'organization_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Department.name'
        db.alter_column('teleforma_department', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'CourseType.description'
        db.alter_column('teleforma_course_type', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'CourseType.name'
        db.alter_column('teleforma_course_type', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Professor.department'
        db.alter_column('teleforma_professor', 'department_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Department'], null=True))

        # Changing field 'Professor.user'
        db.alter_column('teleforma_professor', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Conference.public_id'
        db.alter_column('teleforma_conference', 'public_id', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Conference.room'
        db.alter_column('teleforma_conference', 'room_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.Room']))

        # Changing field 'Conference.course'
        db.alter_column('teleforma_conference', 'course_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Course']))

        # Changing field 'Conference.professor'
        db.alter_column('teleforma_conference', 'professor_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Professor'], null=True))

        # Changing field 'Conference.period'
        db.alter_column('teleforma_conference', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Conference.course_type'
        db.alter_column('teleforma_conference', 'course_type_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.CourseType']))

        # Changing field 'Conference.session'
        db.alter_column('teleforma_conference', 'session', self.gf('telemeta.models.core.CharField')(max_length=16))

        # Changing field 'Conference.department'
        db.alter_column('teleforma_conference', 'department_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Department'], null=True))

        # Changing field 'Conference.date_begin'
        db.alter_column('teleforma_conference', 'date_begin', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'Conference.date_end'
        db.alter_column('teleforma_conference', 'date_end', self.gf('telemeta.models.core.DateTimeField')(null=True))

        # Changing field 'LiveStream.conference'
        db.alter_column('teleforma_live_stream', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'LiveStream.streaming'
        db.alter_column('teleforma_live_stream', 'streaming', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'LiveStream.stream_type'
        db.alter_column('teleforma_live_stream', 'stream_type', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'LiveStream.server'
        db.alter_column('teleforma_live_stream', 'server_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.StreamingServer']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'teleforma.aestudent': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'AEStudent', 'db_table': "'teleforma_ae_student'"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ae_student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ae_student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'ae_student'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'teleforma.conference': {
            'Meta': {'ordering': "['-date_begin']", 'object_name': 'Conference'},
            'comment': ('teleforma.fields.ShortTextField', [], {'max_length': '255', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.CourseType']"}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Department']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Professor']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'teleforma.course': {
            'Meta': {'ordering': "['number']", 'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.BooleanField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.BooleanField', [], {}),
            'synthesis_note': ('django.db.models.fields.BooleanField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_tweeter': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.coursetype': {
            'Meta': {'object_name': 'CourseType', 'db_table': "'teleforma_course_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'default_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'department'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.discount': {
            'Meta': {'object_name': 'Discount', 'db_table': "'teleforma_discounts'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discounts'", 'to': "orm['teleforma.Student']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'annal_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.IEJ']"}),
            'is_annal': ('django.db.models.fields.BooleanField', [], {}),
            'is_published': ('django.db.models.fields.BooleanField', [], {}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'to': "orm['teleforma.DocumentType']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'teleforma.documentsimple': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'DocumentSimple', 'db_table': "'teleforma_document_simple'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document_simple'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document_simple'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'teleforma.documenttype': {
            'Meta': {'ordering': "['number']", 'object_name': 'DocumentType', 'db_table': "'teleforma_document_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'teleforma.iej': {
            'Meta': {'ordering': "['name']", 'object_name': 'IEJ'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.livestream': {
            'Meta': {'object_name': 'LiveStream', 'db_table': "'teleforma_live_stream'"},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'livestream'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'livestream'", 'to': "orm['teleforma.StreamingServer']"}),
            'stream_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'streaming': ('django.db.models.fields.BooleanField', [], {})
        },
        'teleforma.media': {
            'Meta': {'ordering': "['-conference__session', '-date_modified']", 'object_name': 'Media'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'teleforma.optionalfee': {
            'Meta': {'object_name': 'OptionalFee', 'db_table': "'teleforma_optional_fees'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'optional_fees'", 'to': "orm['teleforma.Student']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.payment': {
            'Meta': {'ordering': "['month']", 'object_name': 'Payment', 'db_table': "'teleforma_payments'"},
            'collected': ('django.db.models.fields.BooleanField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['teleforma.Student']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.period': {
            'Meta': {'ordering': "['name']", 'object_name': 'Period'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.professor': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Department']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'teleforma.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'teleforma_profiles'"},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_password': ('django.db.models.fields.BooleanField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'wifi_login': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'wifi_pass': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.streamingserver': {
            'Meta': {'object_name': 'StreamingServer', 'db_table': "'teleforma_streaming_server'"},
            'admin_password': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'source_password': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'teleforma.student': {
            'Meta': {'ordering': "['user__last_name', '-date_subscribed']", 'object_name': 'Student'},
            'application_fees': ('django.db.models.fields.BooleanField', [], {}),
            'confirmation_sent': ('django.db.models.fields.BooleanField', [], {}),
            'date_subscribed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.IEJ']"}),
            'is_subscribed': ('django.db.models.fields.BooleanField', [], {}),
            'options': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'options'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_1'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_2'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_speciality'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('django.db.models.fields.BooleanField', [], {}),
            'procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'procedure'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'subscription_fees': ('django.db.models.fields.FloatField', [], {}),
            'trainings': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'student_trainings'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Training']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'written_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'written_speciality'", 'null': 'True', 'to': "orm['teleforma.Course']"})
        },
        'teleforma.training': {
            'Meta': {'object_name': 'Training'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_magistral'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_obligation'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_options'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_1': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_1'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_2': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_2'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_speciality': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_speciality'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training'", 'null': 'True', 'to': "orm['teleforma.Period']"}),
            'procedure': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_procedure'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'synthesis_note': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_synthesis_note'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'written_speciality': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_written_speciality'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"})
        },
        'telemeta.acquisitionmode': {
            'Meta': {'ordering': "['value']", 'object_name': 'AcquisitionMode', 'db_table': "'acquisition_modes'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.adconversion': {
            'Meta': {'ordering': "['value']", 'object_name': 'AdConversion', 'db_table': "'ad_conversions'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.copytype': {
            'Meta': {'ordering': "['value']", 'object_name': 'CopyType', 'db_table': "'copy_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.ethnicgroup': {
            'Meta': {'ordering': "['value']", 'object_name': 'EthnicGroup', 'db_table': "'ethnic_groups'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.genericstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'GenericStyle', 'db_table': "'generic_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language', 'db_table': "'languages'"},
            'comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'part1': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'part2B': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'part2T': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '3', 'blank': 'True'}),
            'scope': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'}),
            'type': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
        },
        'telemeta.legalright': {
            'Meta': {'ordering': "['value']", 'object_name': 'LegalRight', 'db_table': "'legal_rights'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location', 'db_table': "'locations'"},
            'complete_type': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['telemeta.LocationType']"}),
            'current_location': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'past_names'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Location']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authoritative': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('telemeta.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('telemeta.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'type': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'telemeta.locationtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocationType', 'db_table': "'location_types'"},
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.fields.CharField', [], {'max_length': '150'})
        },
        'telemeta.mediacollection': {
            'Meta': {'ordering': "['code']", 'object_name': 'MediaCollection', 'db_table': "'media_collections'"},
            'acquisition_mode': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AcquisitionMode']"}),
            'ad_conversion': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.AdConversion']"}),
            'alt_copies': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'alt_ids': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'alt_title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'archiver_notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.fields.BooleanField', [], {'default': 'True'}),
            'booklet_author': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'booklet_description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'cnrs_contributor': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collector': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_is_creator': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'conservation_site': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'copy_type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.CopyType']"}),
            'creator': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'description': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'external_references': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'items_done': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'legal_rights': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.LegalRight']"}),
            'media_type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'metadata_author': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataAuthor']"}),
            'metadata_writer': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MetadataWriter']"}),
            'old_code': ('telemeta.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'original_format': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.OriginalFormat']"}),
            'physical_format': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PhysicalFormat']"}),
            'physical_items_num': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'public_access': ('telemeta.models.fields.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publisher': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Publisher']"}),
            'publisher_collection': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublisherCollection']"}),
            'publisher_serial': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'publishing_status': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.PublishingStatus']"}),
            'recorded_from_year': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recorded_to_year': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'recording_context': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.RecordingContext']"}),
            'reference': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'status': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'collections'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Status']"}),
            'title': ('telemeta.models.fields.CharField', [], {'max_length': '250'}),
            'travail': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'year_published': ('telemeta.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telemeta.mediaitem': {
            'Meta': {'object_name': 'MediaItem', 'db_table': "'media_items'"},
            'alt_title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'approx_duration': ('telemeta.models.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'author': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'auto_period_access': ('telemeta.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'collection': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.fields.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contributor': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'creator_reference': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'depositor': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitalist': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'digitization_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.fields.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
            'location': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'media_type': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaType']"}),
            'mimetype': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'old_code': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'organization': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Organization']", 'null': 'True', 'blank': 'True'}),
            'public_access': ('telemeta.models.fields.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'publishing_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recordist': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'rights': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Rights']", 'null': 'True', 'blank': 'True'}),
            'scientist': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'summary': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'topic': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Topic']", 'null': 'True', 'blank': 'True'}),
            'track': ('telemeta.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'vernacular_style': ('telemeta.models.fields.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.VernacularStyle']"})
        },
        'telemeta.mediatype': {
            'Meta': {'ordering': "['value']", 'object_name': 'MediaType', 'db_table': "'media_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadataauthor': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataAuthor', 'db_table': "'metadata_authors'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.metadatawriter': {
            'Meta': {'ordering': "['value']", 'object_name': 'MetadataWriter', 'db_table': "'metadata_writers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.organization': {
            'Meta': {'ordering': "['value']", 'object_name': 'Organization', 'db_table': "'organization'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.originalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'OriginalFormat', 'db_table': "'original_format'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.physicalformat': {
            'Meta': {'ordering': "['value']", 'object_name': 'PhysicalFormat', 'db_table': "'physical_formats'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publisher': {
            'Meta': {'ordering': "['value']", 'object_name': 'Publisher', 'db_table': "'publishers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.publishercollection': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublisherCollection', 'db_table': "'publisher_collections'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('telemeta.models.fields.ForeignKey', [], {'related_name': "'publisher_collections'", 'to': "orm['telemeta.Publisher']"}),
            'value': ('telemeta.models.fields.CharField', [], {'max_length': '250'})
        },
        'telemeta.publishingstatus': {
            'Meta': {'ordering': "['value']", 'object_name': 'PublishingStatus', 'db_table': "'publishing_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.recordingcontext': {
            'Meta': {'ordering': "['value']", 'object_name': 'RecordingContext', 'db_table': "'recording_contexts'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.rights': {
            'Meta': {'ordering': "['value']", 'object_name': 'Rights', 'db_table': "'rights'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.status': {
            'Meta': {'ordering': "['value']", 'object_name': 'Status', 'db_table': "'media_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.topic': {
            'Meta': {'ordering': "['value']", 'object_name': 'Topic', 'db_table': "'topic'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('telemeta.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'value': ('telemeta.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['teleforma']