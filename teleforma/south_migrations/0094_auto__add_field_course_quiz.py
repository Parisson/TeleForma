# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.quiz'
        db.add_column('teleforma_course', 'quiz',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Course.quiz'
        db.delete_column('teleforma_course', 'quiz_id')


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
        'teleforma.aestudent': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'AEStudent', 'db_table': "'teleforma_ae_student'"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ae_student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ae_student'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'ae_student'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.conference': {
            'Meta': {'ordering': "['-date_begin']", 'object_name': 'Conference'},
            'comment': ('teleforma.fields.ShortTextField', [], {'max_length': '255', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.CourseType']"}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Professor']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'web_class_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conferences'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.WebClassGroup']"})
        },
        'teleforma.course': {
            'Meta': {'ordering': "['number']", 'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'has_exam_scripts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oral_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oral_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oral_speciality': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'procedure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Quiz']", 'null': 'True', 'blank': 'True'}),
            'synthesis_note': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_tweeter': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'written_speciality': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.coursegroup': {
            'Meta': {'object_name': 'CourseGroup', 'db_table': "'teleforma_course_group'"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'course_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
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
            'default_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'departments'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.discount': {
            'Meta': {'object_name': 'Discount', 'db_table': "'teleforma_discounts'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discounts'", 'to': "orm['teleforma.Student']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'annal_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'document'", 'blank': 'True', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.IEJ']"}),
            'is_annal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'periods': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'documents'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Period']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
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
            'file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '1024', 'db_column': "'filename'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document_simple'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'document_simple'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'teleforma.documenttype': {
            'Meta': {'ordering': "['number']", 'object_name': 'DocumentType', 'db_table': "'teleforma_document_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'teleforma.groupedmessage': {
            'Meta': {'object_name': 'GroupedMessage', 'db_table': "'teleforma_grouped_messages'"},
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grouped_messages'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.StudentGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grouped_messages'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '119'}),
            'to_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.home': {
            'Meta': {'object_name': 'Home'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teleforma.Media']", 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "['-date_modified', '-conference__session']", 'object_name': 'Media'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Conference']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['teleforma.CourseType']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'to': "orm['telemeta.MediaItem']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'media'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'teleforma.optionalfee': {
            'Meta': {'object_name': 'OptionalFee', 'db_table': "'teleforma_optional_fees'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'optional_fees'", 'to': "orm['teleforma.Student']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.payback': {
            'Meta': {'object_name': 'Payback', 'db_table': "'teleforma_paybacks'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paybacks'", 'to': "orm['teleforma.Student']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.payment': {
            'Meta': {'ordering': "['month']", 'object_name': 'Payment', 'db_table': "'teleforma_payments'"},
            'collected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['teleforma.Student']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'teleforma.period': {
            'Meta': {'ordering': "['name']", 'object_name': 'Period'},
            'date_begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_exam_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_password_init': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'period'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'message_local': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'message_platform': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['teleforma.Period']"})
        },
        'teleforma.professor': {
            'Meta': {'ordering': "['user__last_name']", 'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'teleforma_profiles'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'wifi_login': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'wifi_pass': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
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
            'Meta': {'ordering': "['user__last_name', '-date_subscribed']", 'object_name': 'Student'},
            'application_fees': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmation_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_subscribed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iej': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.IEJ']"}),
            'is_subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'options': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'options_students'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_1_students'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_2_students'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'oral_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oral_speciality_students'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Period']"}),
            'platform_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'procedure_students'", 'null': 'True', 'to': "orm['teleforma.Course']"}),
            'promo_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'subscription_fees': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'student_training'", 'null': 'True', 'to': "orm['teleforma.Training']"}),
            'trainings': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'student_trainings'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Training']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'written_speciality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'written_speciality_2students'", 'null': 'True', 'to': "orm['teleforma.Course']"})
        },
        'teleforma.studentgroup': {
            'Meta': {'object_name': 'StudentGroup', 'db_table': "'teleforma_student_groups'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Student']"})
        },
        'teleforma.training': {
            'Meta': {'object_name': 'Training'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_magistral'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_obligation'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_options'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_1': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_1'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_2': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_2'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'oral_speciality': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_oral_speciality'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['teleforma.Training']"}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training'", 'null': 'True', 'to': "orm['teleforma.Period']"}),
            'procedure': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_procedure'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'synthesis_note': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_synthesis_note'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"}),
            'written_speciality': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'training_written_speciality'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.CourseType']"})
        },
        'teleforma.webclassgroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'WebClassGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iejs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'web_class_group'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.IEJ']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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