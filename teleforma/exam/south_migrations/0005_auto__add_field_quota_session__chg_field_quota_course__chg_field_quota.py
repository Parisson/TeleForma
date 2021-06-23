# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Quota.session'
        db.add_column('exam_quota', 'session',
                      self.gf('django.db.models.fields.CharField')(default='1', max_length=16),
                      keep_default=False)


        # Changing field 'Quota.course'
        db.alter_column('exam_quota', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['teleforma.Course']))

        # Changing field 'Quota.corrector'
        db.alter_column('exam_quota', 'corrector_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

    def backwards(self, orm):
        # Deleting field 'Quota.session'
        db.delete_column('exam_quota', 'session')


        # Changing field 'Quota.course'
        db.alter_column('exam_quota', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Course']))

        # Changing field 'Quota.corrector'
        db.alter_column('exam_quota', 'corrector_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

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
        'exam.quota': {
            'Meta': {'ordering': "['-date_end']", 'object_name': 'Quota'},
            'corrector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quotas'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quotas'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Course']"}),
            'date_end': ('django.db.models.fields.DateField', [], {}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quotas'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'script_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quotas'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['exam.ScriptType']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'exam.script': {
            'Meta': {'ordering': "['date_added']", 'object_name': 'Script'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'author_scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'box_uuid': ('django.db.models.fields.CharField', [], {'max_length': "'256'", 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'corrector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'corrector_scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Course']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_marked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'date_rejected': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'reject_reason': ('django.db.models.fields.CharField', [], {'max_length': "'256'", 'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scripts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['exam.ScriptType']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': "'2048'", 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'exam.scriptpage': {
            'Meta': {'object_name': 'ScriptPage'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['exam.Script']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'exam.scripttype': {
            'Meta': {'object_name': 'ScriptType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'512'", 'blank': 'True'})
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
            'oral_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oral_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oral_speciality': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'procedure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'synthesis_note': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_tweeter': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'written_speciality': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'default_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'department'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.period': {
            'Meta': {'ordering': "['name']", 'object_name': 'Period'},
            'date_begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_password_init': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_local': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'message_platform': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['teleforma.Period']"})
        }
    }

    complete_apps = ['exam']