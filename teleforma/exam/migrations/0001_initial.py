# Generated by Django 3.2.3 on 2021-06-01 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teleforma', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='date modified')),
                ('uuid', models.CharField(blank=True, max_length=512, verbose_name='UUID')),
                ('mime_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='MIME type')),
                ('sha1', models.CharField(blank=True, max_length=512, verbose_name='sha1')),
                ('session', models.CharField(default='1', max_length=16, verbose_name='session')),
                ('file', models.FileField(blank=True, max_length=1024, upload_to='scripts/%Y/%m/%d', verbose_name='PDF file')),
                ('box_uuid', models.CharField(blank=True, max_length=256, verbose_name='Box UUID')),
                ('score', models.FloatField(blank=True, help_text='/20', null=True, verbose_name='score')),
                ('comments', models.TextField(blank=True, verbose_name='comments')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'rejected'), (1, 'draft'), (2, 'submitted'), (3, 'pending'), (4, 'marked'), (5, 'read'), (6, 'backup'), (7, 'stat')], verbose_name='status')),
                ('reject_reason', models.CharField(blank=True, choices=[('unreadable', 'unreadable'), ('bad orientation', 'bad orientation'), ('bad framing', 'bad framing'), ('incomplete', 'incomplete'), ('wrong course', 'wrong course'), ('duplicate', 'duplicate'), ('other', 'other'), ('wrong format', 'wrong format'), ('unreadable file', 'unreadable file'), ('no file', 'no file'), ('error retrieving file', 'error retrieving file'), ('file too large', 'file too large')], max_length=256, verbose_name='reason')),
                ('date_submitted', models.DateTimeField(blank=True, null=True, verbose_name='date submitted')),
                ('date_marked', models.DateTimeField(blank=True, null=True, verbose_name='date marked')),
                ('date_rejected', models.DateTimeField(blank=True, null=True, verbose_name='date rejected')),
                ('url', models.CharField(blank=True, max_length=2048, verbose_name='URL')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_scripts', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('corrector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corrector_scripts', to=settings.AUTH_USER_MODEL, verbose_name='corrector')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scripts', to='teleforma.course', verbose_name='course')),
                ('period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scripts', to='teleforma.period', verbose_name='period')),
            ],
            options={
                'verbose_name': 'Script',
                'verbose_name_plural': 'Scripts',
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='ScriptType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512, verbose_name='name')),
            ],
            options={
                'verbose_name': 'ScriptType',
                'verbose_name_plural': 'ScriptTypes',
            },
        ),
        migrations.CreateModel(
            name='ScriptPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='date modified')),
                ('uuid', models.CharField(blank=True, max_length=512, verbose_name='UUID')),
                ('mime_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='MIME type')),
                ('sha1', models.CharField(blank=True, max_length=512, verbose_name='sha1')),
                ('file', models.FileField(blank=True, max_length=1024, upload_to='script_pages/%Y/%m/%d', verbose_name='Page file')),
                ('image', models.ImageField(blank=True, upload_to='script_pages/%Y/%m/%d', verbose_name='Image file')),
                ('rank', models.IntegerField(blank=True, null=True, verbose_name='rank')),
                ('script', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='exam.script', verbose_name='script')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.AddField(
            model_name='script',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scripts', to='exam.scripttype', verbose_name='type'),
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15')], default='1', max_length=16, verbose_name='session')),
                ('value', models.IntegerField(verbose_name='value')),
                ('date_start', models.DateField(verbose_name='date start')),
                ('date_end', models.DateField(verbose_name='date end')),
                ('corrector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotas', to=settings.AUTH_USER_MODEL, verbose_name='corrector')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotas', to='teleforma.course', verbose_name='course')),
                ('period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotas', to='teleforma.period', verbose_name='period')),
                ('script_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotas', to='exam.scripttype', verbose_name='type')),
            ],
            options={
                'verbose_name': 'Quota',
                'verbose_name_plural': 'Quotas',
                'ordering': ['-date_end'],
            },
        ),
    ]
