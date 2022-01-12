# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from teleforma.models.core import MediaTranscoded


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MediaTranscoded'
        db.create_table('teleforma_media_transcoded', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transcoded', to=orm['teleforma.Media'])),
            ('mimetype', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal('teleforma', ['MediaTranscoded'])


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
        # Adding field 'Media.file'
        db.add_column('teleforma_media', 'file',
                      self.gf('django.db.models.fields.files.FileField')(max_length=1024, null=True),
                      keep_default=False)

        # Adding field 'Media.poster_file'
        db.add_column('teleforma_media', 'poster_file',
                      self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True),
                      keep_default=False)


        # Changing field 'Media.conference'
        db.alter_column('teleforma_media', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Conference']))

        # Changing field 'Media.code'
        db.alter_column('teleforma_media', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.description'
        db.alter_column('teleforma_media', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Media.title'
        db.alter_column('teleforma_media', 'title', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Changing field 'Media.date_modified'
        db.alter_column('teleforma_media', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2021, 11, 17, 0, 0)))

        # Changing field 'Media.period'
        db.alter_column('teleforma_media', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Media.rank'
        db.alter_column('teleforma_media', 'rank', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Media.course_type'
        db.alter_column('teleforma_media', 'course_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.CourseType']))

        # Changing field 'Media.course'
        db.alter_column('teleforma_media', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Media.item'
        db.alter_column('teleforma_media', 'item_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telemeta.MediaItem']))

        # Changing field 'Media.date_added'
        db.alter_column('teleforma_media', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2021, 11, 17, 0, 0)))

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

        # Changing field 'Course.title'
        db.alter_column('teleforma_course', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Course.date_modified'
        db.alter_column('teleforma_course', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

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

        # Changing field 'Document.code'
        db.alter_column('teleforma_document', 'code', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.description'
        db.alter_column('teleforma_document', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.title'
        db.alter_column('teleforma_document', 'title', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Changing field 'Document.date_modified'
        db.alter_column('teleforma_document', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2021, 11, 17, 0, 0)))

        # Changing field 'Document.period'
        db.alter_column('teleforma_document', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

        # Changing field 'Document.credits'
        db.alter_column('teleforma_document', 'credits', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.course'
        db.alter_column('teleforma_document', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Course']))

        # Changing field 'Document.file'
        db.alter_column('teleforma_document', 'filename', self.gf('django.db.models.fields.files.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'Document.date_added'
        db.alter_column('teleforma_document', 'date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2021, 11, 17, 0, 0)))

        # Changing field 'Document.is_published'
        db.alter_column('teleforma_document', 'is_published', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Document.type'
        db.alter_column('teleforma_document', 'type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.DocumentType']))

        # Changing field 'Document.mime_type'
        db.alter_column('teleforma_document', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Document.is_annal'
        db.alter_column('teleforma_document', 'is_annal', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'CourseDomain.name'
        db.alter_column('teleforma_domain', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'IEJ.description'
        db.alter_column('teleforma_iej', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'IEJ.name'
        db.alter_column('teleforma_iej', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Seminar.duration'
        db.alter_column('teleforma_seminar', 'duration', self.gf('teleforma.fields.DurationField')())

        # Changing field 'Seminar.period'
        db.alter_column('teleforma_seminar', 'period_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Period']))

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
        db.alter_column('teleforma_student', 'iej_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.IEJ']))

        # Changing field 'Student.user'
        db.alter_column('teleforma_student', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Student.options'
        db.alter_column('teleforma_student', 'options_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.written_speciality'
        db.alter_column('teleforma_student', 'written_speciality_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Student.procedure'
        db.alter_column('teleforma_student', 'procedure_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'AEStudent.user'
        db.alter_column('teleforma_ae_student', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'AEStudent.platform_only'
        db.alter_column('teleforma_ae_student', 'platform_only', self.gf('django.db.models.fields.BooleanField')())

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

        # Changing field 'Department.domain'
        db.alter_column('teleforma_department', 'domain', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Department.description'
        db.alter_column('teleforma_department', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Department.organization'
        db.alter_column('teleforma_department', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Department.name'
        db.alter_column('teleforma_department', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'CourseType.description'
        db.alter_column('teleforma_course_type', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'CourseType.name'
        db.alter_column('teleforma_course_type', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Professor.user'
        db.alter_column('teleforma_professor', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Professor.title'
        db.alter_column('teleforma_professor', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Conference.duration'
        db.alter_column('teleforma_conference', 'duration', self.gf('teleforma.fields.DurationField')())

        # Changing field 'Conference.city'
        db.alter_column('teleforma_conference', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['telemeta.Location']))

        # Changing field 'Conference.location'
        db.alter_column('teleforma_conference', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['telemeta.Location']))

        # Changing field 'Conference.webclass_hours_complementary'
        db.alter_column('teleforma_conference', 'webclass_hours_complementary', self.gf('teleforma.fields.DurationField')())

        # Changing field 'LiveStream.conference'
        db.alter_column('teleforma_live_stream', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Conference']))

        # Changing field 'LiveStream.streaming'
        db.alter_column('teleforma_live_stream', 'streaming', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'LiveStream.stream_type'
        db.alter_column('teleforma_live_stream', 'stream_type', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'LiveStream.server'
        db.alter_column('teleforma_live_stream', 'server_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teleforma.StreamingServer']))

        # Adding field 'Media.approx_duration'
        db.add_column('teleforma_media', 'approx_duration',
                      self.gf('teleforma.fields.DurationField')(default='0', blank=True),
                      keep_default=False)

        if not db.dry_run:
            from teleforma.models.core import Media

            for media_item in Media.objects.all():
                # set file directly on mediaitem
                media_item.file = media_item.item.file
                # get poster file
                try:
                    media_item.poster_file = media_item.item.related.filter(title="preview")[0].file
                except IndexError:
                    pass
                media_item.approx_duration = media_item.item.approx_duration
                if not media_item.title:
                    media_item.title = media_item.item.title

                media_item.save()

                for transcode_item in media_item.item.transcoded.filter():
                    transcoded = MediaTranscoded(
                        item=media_item, 
                        mimetype=transcode_item.mime_type, 
                        date_added=transcode_item.date_added, 
                        status=transcode_item.status,
                        file=transcode_item.file
                        )
                    transcoded.save()

                # # add media transcoded : original CRFPA code
                # for item in Media.objects.filter(conference=media_item.conference, course=media_item.course, course_type=media_item.course_type, period=media_item.period):
                #     if item.id == media_item.id:
                #         continue

                #     transcoded = MediaTranscoded(
                #         item=media_item, 
                #         mimetype=item.mime_type, 
                #         date_added=item.date_added, 
                #         status=5,
                #         file=item.item.file
                #         )
                #     transcoded.save()
                #     # remove transcoded item from Media
                #     item.delete()

                    
    def backwards(self, orm):
        # Deleting model 'MediaTranscoded'
        db.delete_table('teleforma_media_transcoded')


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
        # Deleting field 'Media.file'
        db.delete_column('teleforma_media', 'file')

        # Deleting field 'Media.poster_file'
        db.delete_column('teleforma_media', 'poster_file')


        # Changing field 'Media.conference'
        db.alter_column('teleforma_media', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'Media.code'
        db.alter_column('teleforma_media', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.description'
        db.alter_column('teleforma_media', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Media.title'
        db.alter_column('teleforma_media', 'title', self.gf('telemeta.models.core.CharField')(max_length=1024))

        # Changing field 'Media.date_modified'
        db.alter_column('teleforma_media', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Media.period'
        db.alter_column('teleforma_media', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Media.rank'
        db.alter_column('teleforma_media', 'rank', self.gf('telemeta.models.core.IntegerField')(null=True))

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

        # Changing field 'Course.title'
        db.alter_column('teleforma_course', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Course.date_modified'
        db.alter_column('teleforma_course', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

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

        # Changing field 'Document.code'
        db.alter_column('teleforma_document', 'code', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.description'
        db.alter_column('teleforma_document', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.title'
        db.alter_column('teleforma_document', 'title', self.gf('telemeta.models.core.CharField')(max_length=1024))

        # Changing field 'Document.date_modified'
        db.alter_column('teleforma_document', 'date_modified', self.gf('telemeta.models.core.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Document.period'
        db.alter_column('teleforma_document', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

        # Changing field 'Document.credits'
        db.alter_column('teleforma_document', 'credits', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.course'
        db.alter_column('teleforma_document', 'course_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Course'], null=True))

        # Changing field 'Document.file'
        db.alter_column('teleforma_document', 'filename', self.gf('telemeta.models.core.FileField')(max_length=1024, db_column='filename'))

        # Changing field 'Document.date_added'
        db.alter_column('teleforma_document', 'date_added', self.gf('telemeta.models.core.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Document.is_published'
        db.alter_column('teleforma_document', 'is_published', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'Document.type'
        db.alter_column('teleforma_document', 'type_id', self.gf('telemeta.models.core.ForeignKey')(null=True, to=orm['teleforma.DocumentType']))

        # Changing field 'Document.mime_type'
        db.alter_column('teleforma_document', 'mime_type', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Document.is_annal'
        db.alter_column('teleforma_document', 'is_annal', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'CourseDomain.name'
        db.alter_column('teleforma_domain', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'IEJ.description'
        db.alter_column('teleforma_iej', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'IEJ.name'
        db.alter_column('teleforma_iej', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Seminar.duration'
        db.alter_column('teleforma_seminar', 'duration', self.gf('telemeta.models.core.DurationField')())

        # Changing field 'Seminar.period'
        db.alter_column('teleforma_seminar', 'period_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Period'], null=True))

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

        # Changing field 'Department.domain'
        db.alter_column('teleforma_department', 'domain', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Department.description'
        db.alter_column('teleforma_department', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Department.organization'
        db.alter_column('teleforma_department', 'organization_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.Organization']))

        # Changing field 'Department.name'
        db.alter_column('teleforma_department', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'CourseType.description'
        db.alter_column('teleforma_course_type', 'description', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'CourseType.name'
        db.alter_column('teleforma_course_type', 'name', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Professor.user'
        db.alter_column('teleforma_professor', 'user_id', self.gf('telemeta.models.core.ForeignKey')(unique=True, to=orm['auth.User']))

        # Changing field 'Professor.title'
        db.alter_column('teleforma_professor', 'title', self.gf('telemeta.models.core.CharField')(max_length=255))

        # Changing field 'Conference.duration'
        db.alter_column('teleforma_conference', 'duration', self.gf('telemeta.models.core.DurationField')())

        # Changing field 'Conference.city'
        db.alter_column('teleforma_conference', 'city_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.Location']))

        # Changing field 'Conference.location'
        db.alter_column('teleforma_conference', 'location_id', self.gf('telemeta.models.core.WeakForeignKey')(null=True, to=orm['telemeta.Location']))

        # Changing field 'Conference.webclass_hours_complementary'
        db.alter_column('teleforma_conference', 'webclass_hours_complementary', self.gf('telemeta.models.core.DurationField')())

        # Changing field 'LiveStream.conference'
        db.alter_column('teleforma_live_stream', 'conference_id', self.gf('telemeta.models.core.ForeignKey')(on_delete=models.SET_NULL, to=orm['teleforma.Conference'], null=True))

        # Changing field 'LiveStream.streaming'
        db.alter_column('teleforma_live_stream', 'streaming', self.gf('telemeta.models.core.BooleanField')())

        # Changing field 'LiveStream.stream_type'
        db.alter_column('teleforma_live_stream', 'stream_type', self.gf('telemeta.models.core.CharField')(max_length=32))

        # Changing field 'LiveStream.server'
        db.alter_column('teleforma_live_stream', 'server_id', self.gf('telemeta.models.core.ForeignKey')(to=orm['teleforma.StreamingServer']))

        # Deleting field 'Media.approx_duration'
        db.delete_column('teleforma_media', 'approx_duration')

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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forms.form': {
            'Meta': {'object_name': 'Form'},
            'button_text': ('django.db.models.fields.CharField', [], {'default': "u'Submit'", 'max_length': '50'}),
            'email_copies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email_from': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[1]', 'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2021, 11, 17, 0, 0)'}),
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
        'quiz.category': {
            'Meta': {'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'answers_at_end': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Category']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exam_paper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fail_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_questions': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pass_mark': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'random_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'single_attempt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '60'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'teleforma.aestudent': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'AEStudent', 'db_table': "'teleforma_ae_student'"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ae_student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ae_student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ae_student'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.answer': {
            'Meta': {'ordering': "['-date_submitted', '-date_validated']", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'date_validated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer'", 'to': "orm['teleforma.Question']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'treated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer'", 'to': "orm['auth.User']"}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.auditor': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'Auditor'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'block_fifpl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'block_testimonials': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conferences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'auditor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Conference']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fifpl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'platform_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'seminars': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'auditor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Seminar']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auditor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.conference': {
            'Meta': {'ordering': "['-date_begin']", 'object_name': 'Conference'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'additional_info': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'banner_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'city'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['telemeta.Location']"}),
            'comment': ('teleforma.fields.ShortTextField', [], {'max_length': '255', 'blank': 'True'}),
            'concerned': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'to': "orm['teleforma.CourseType']"}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'docs_description': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference_docs_description'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Document']"}),
            'duration': ('teleforma.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'location'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['telemeta.Location']"}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'plan': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Professor']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'suggested_conferences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conferences_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Conference']"}),
            'suggested_seminars': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conferences_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Seminar']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'upcoming': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vignette_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'webclass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'webclass_hours_complementary': ('teleforma.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'webclass_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'webclass_max_participants': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'webclass_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'teleforma.course': {
            'Meta': {'ordering': "['number']", 'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'synthesis_note': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'course'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"})
        },
        'teleforma.coursedomain': {
            'Meta': {'object_name': 'CourseDomain', 'db_table': "'teleforma_domain'"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'domain'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.coursetype': {
            'Meta': {'object_name': 'CourseType', 'db_table': "'teleforma_course_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'address': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"}),
            'signature': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'teleforma.document': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Document'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_annal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'to': "orm['teleforma.DocumentType']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        'teleforma.documenttype': {
            'Meta': {'ordering': "['number']", 'object_name': 'DocumentType', 'db_table': "'teleforma_document_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'teleforma.iej': {
            'Meta': {'ordering': "['name']", 'object_name': 'IEJ'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.livestream': {
            'Meta': {'object_name': 'LiveStream', 'db_table': "'teleforma_live_stream'"},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'livestream'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'livestream'", 'to': "orm['teleforma.StreamingServer']"}),
            'stream_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'streaming': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.media': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Media'},
            'approx_duration': ('teleforma.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'poster_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        'teleforma.mediatranscoded': {
            'Meta': {'object_name': 'MediaTranscoded', 'db_table': "'teleforma_media_transcoded'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transcoded'", 'to': "orm['teleforma.Media']"}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.period': {
            'Meta': {'object_name': 'Period'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.professor': {
            'Meta': {'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portrait': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'teleforma_profiles'"},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.question': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Question'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_nchar': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seminar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question'", 'to': "orm['teleforma.Seminar']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'teleforma.quizvalidation': {
            'Meta': {'ordering': "['-date_validated']", 'object_name': 'QuizValidation', 'db_table': "'teleforma_quiz_validation'"},
            'date_validated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quiz_validation'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['quiz.Quiz']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quiz_validation'", 'to': "orm['auth.User']"}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.seminar': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Seminar'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'additional_info': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'banner_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'concerned': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seminar'", 'to': "orm['teleforma.Course']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_forced': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'docs_1': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminar_docs_1'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Document']"}),
            'docs_2': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminar_docs_2'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Document']"}),
            'docs_correct': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminar_docs_correct'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Document']"}),
            'docs_description': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminar_docs_description'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Document']"}),
            'duration': ('teleforma.fields.DurationField', [], {'default': "'0'", 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'to': "orm['forms.Form']"}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'index': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'magistral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'media_preview': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seminar_preview'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Media']"}),
            'medias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Media']"}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'plan': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'professor': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Professor']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['quiz.Quiz']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'suggested_conferences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminars_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Conference']"}),
            'suggested_seminars': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'seminars_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Seminar']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seminar'", 'null': 'True', 'to': "orm['teleforma.SeminarType']"}),
            'upcoming': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vignette_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'teleforma.seminarrevision': {
            'Meta': {'ordering': "['-date']", 'object_name': 'SeminarRevision', 'db_table': "'teleforma_seminar_revisions'"},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seminar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revision'", 'to': "orm['teleforma.Seminar']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revision'", 'to': "orm['auth.User']"})
        },
        'teleforma.seminartype': {
            'Meta': {'object_name': 'SeminarType', 'db_table': "'teleforma_seminar_type'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.streamingserver': {
            'Meta': {'object_name': 'StreamingServer', 'db_table': "'teleforma_streaming_server'"},
            'admin_password': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'source_password': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'teleforma.student': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'Student'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.IEJ']"}),
            'options': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'options'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_1'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_2'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_speciality'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'period': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'procedure'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['teleforma.Training']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'written_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'written_speciality'", 'null': 'True', 'to': "orm['teleforma.Course']"})
        },
        'teleforma.testimonial': {
            'Meta': {'ordering': "['date_modified', '-date_added']", 'object_name': 'Testimonial'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seminar': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'testimonial'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Seminar']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'testimonial'", 'null': 'True', 'to': "orm['teleforma.TestimonialTemplate']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'testimonial'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"})
        },
        'teleforma.testimonialtemplate': {
            'Meta': {'object_name': 'TestimonialTemplate', 'db_table': "'teleforma_testimonial_template'"},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testimonial_template'", 'to': "orm['teleforma.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testimonial_template'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.training': {
            'Meta': {'object_name': 'Training'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'auto_period_access': ('telemeta.models.core.BooleanField', [], {'default': 'True'}),
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
            'auto_period_access': ('telemeta.models.core.BooleanField', [], {'default': 'True'}),
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
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
            'location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'mimetype': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
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