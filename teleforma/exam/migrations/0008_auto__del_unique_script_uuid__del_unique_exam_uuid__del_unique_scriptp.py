# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ScriptPage', fields ['uuid']
        db.delete_unique('exam_scriptpage', ['uuid'])

        # Removing unique constraint on 'Exam', fields ['uuid']
        db.delete_unique('exam_exam', ['uuid'])

        # Removing unique constraint on 'Script', fields ['uuid']
        db.delete_unique('exam_script', ['uuid'])


    def backwards(self, orm):
        # Adding unique constraint on 'Script', fields ['uuid']
        db.create_unique('exam_script', ['uuid'])

        # Adding unique constraint on 'Exam', fields ['uuid']
        db.create_unique('exam_exam', ['uuid'])

        # Adding unique constraint on 'ScriptPage', fields ['uuid']
        db.create_unique('exam_scriptpage', ['uuid'])


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
        'exam.corrector': {
            'Meta': {'object_name': 'Corrector'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'correctors'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'exam.exam': {
            'Meta': {'object_name': 'Exam'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exams'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exams'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Course']"}),
            'credits': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'exam.quota': {
            'Meta': {'ordering': "['date_start']", 'object_name': 'Quota'},
            'corrector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quotas'", 'null': 'True', 'to': "orm['exam.Corrector']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quotas'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'date_end': ('django.db.models.fields.DateField', [], {}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'exam.script': {
            'Meta': {'object_name': 'Script'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'box_session_key': ('django.db.models.fields.CharField', [], {'max_length': "'1024'", 'blank': 'True'}),
            'box_uuid': ('django.db.models.fields.CharField', [], {'max_length': "'256'", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'corrector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['exam.Corrector']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_corrected': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['exam.Exam']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'reject_reason': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'exam.scriptpage': {
            'Meta': {'object_name': 'ScriptPage'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['exam.Script']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 22, 0, 0)'}),
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
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title_tweeter': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'default_period': ('telemeta.models.core.ForeignKey', [], {'related_name': "'department'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.Period']", 'blank': 'True', 'null': 'True'}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'domain': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'organization': ('telemeta.models.core.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.period': {
            'Meta': {'object_name': 'Period'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['exam']