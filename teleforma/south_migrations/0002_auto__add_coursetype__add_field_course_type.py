# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseType'
        db.create_table('teleforma_course_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('teleforma', ['CourseType'])

        # Adding field 'Course.type'
        db.add_column('teleforma_course', 'type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='course', to=orm['teleforma.CourseType']),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'CourseType'
        db.delete_table('teleforma_course_type')

        # Deleting field 'Course.type'
        db.delete_column('teleforma_course', 'type_id')

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
        'teleforma.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.conference': {
            'Meta': {'object_name': 'Conference'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Professor']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'})
        },
        'teleforma.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.CourseType']"})
        },
        'teleforma.coursetype': {
            'Meta': {'object_name': 'CourseType', 'db_table': "'teleforma_course_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document'", 'to': "orm['teleforma.Course']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_annal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.iej': {
            'Meta': {'object_name': 'IEJ'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.media': {
            'Meta': {'object_name': 'Media'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media'", 'to': "orm['teleforma.Course']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['telemeta.MediaItem']"})
        },
        'teleforma.oral': {
            'Meta': {'object_name': 'Oral'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.procedure': {
            'Meta': {'object_name': 'Procedure'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.professor': {
            'Meta': {'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'teleforma_profiles'"},
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.speciality': {
            'Meta': {'object_name': 'Speciality'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.student': {
            'Meta': {'object_name': 'Student'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['teleforma.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['teleforma.IEJ']"}),
            'oral_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_1'", 'null': 'True', 'to': "orm['teleforma.Oral']"}),
            'oral_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_2'", 'null': 'True', 'to': "orm['teleforma.Oral']"}),
            'oral_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student_oral_spe'", 'null': 'True', 'to': "orm['teleforma.Speciality']"}),
            'procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'to': "orm['teleforma.Procedure']"}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'to': "orm['teleforma.Training']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'written_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student_written_spe'", 'null': 'True', 'to': "orm['teleforma.Speciality']"})
        },
        'teleforma.training': {
            'Meta': {'object_name': 'Training'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'synthesis_note': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'language_iso': ('telemeta.models.core.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['telemeta.Language']", 'blank': 'True', 'null': 'True'}),
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