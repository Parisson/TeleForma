# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Media'
        db.delete_table('teleforma_media')

        # Adding model 'Audio'
        db.create_table('teleforma_audio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('credits', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='audio', to=orm['teleforma.Course'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='audio', to=orm['telemeta.MediaItem'])),
        ))
        db.send_create_signal('teleforma', ['Audio'])

        # Adding model 'Video'
        db.create_table('teleforma_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('credits', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video', to=orm['teleforma.Course'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video', to=orm['telemeta.MediaItem'])),
        ))
        db.send_create_signal('teleforma', ['Video'])

    def backwards(self, orm):
        # Adding model 'Media'
        db.create_table('teleforma_media', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media', to=orm['teleforma.Course'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media', to=orm['telemeta.MediaItem'])),
            ('credits', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('teleforma', ['Media'])

        # Deleting model 'Audio'
        db.delete_table('teleforma_audio')

        # Deleting model 'Video'
        db.delete_table('teleforma_video')

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
        'teleforma.audio': {
            'Meta': {'object_name': 'Audio'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audio'", 'to': "orm['teleforma.Course']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'audio'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.conference': {
            'Meta': {'object_name': 'Conference'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Professor']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Category']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.document': {
            'Meta': {'object_name': 'Document'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document'", 'to': "orm['teleforma.Course']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'filename'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.iej': {
            'Meta': {'object_name': 'IEJ'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.professor': {
            'Meta': {'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professor'", 'to': "orm['auth.User']"})
        },
        'teleforma.student': {
            'Meta': {'object_name': 'Student'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['teleforma.Category']"}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['teleforma.IEJ']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['auth.User']"})
        },
        'teleforma.video': {
            'Meta': {'object_name': 'Video'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video'", 'to': "orm['teleforma.Course']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video'", 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'00:00'", 'blank': 'True'}),
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
            'approx_duration': ('telemeta.models.core.DurationField', [], {'default': "'00:00'", 'blank': 'True'}),
            'author': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '250', 'blank': 'True'}),
            'collection': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'to': "orm['telemeta.MediaCollection']"}),
            'collector': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'collector_from_collection': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'collector_selection': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'context_comment': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'copied_from_item': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'copies'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'creator_reference': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'cultural_area': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'ethnic_group': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.EthnicGroup']"}),
            'external_references': ('telemeta.models.core.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '100', 'db_column': "'filename'", 'blank': 'True'}),
            'generic_style': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.GenericStyle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['telemeta.Language']"}),
            'location': ('telemeta.models.core.WeakForeignKey', [], {'default': 'None', 'to': "orm['telemeta.Location']", 'null': 'True', 'blank': 'True'}),
            'location_comment': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'moda_execut': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'old_code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'public_access': ('telemeta.models.core.CharField', [], {'default': "'metadata'", 'max_length': '16', 'blank': 'True'}),
            'recorded_from_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'recorded_to_date': ('telemeta.models.core.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
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
        'telemeta.vernacularstyle': {
            'Meta': {'ordering': "['value']", 'object_name': 'VernacularStyle', 'db_table': "'vernacular_styles'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('telemeta.models.core.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['teleforma']