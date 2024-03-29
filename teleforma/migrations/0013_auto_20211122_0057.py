# Generated by Django 3.2.3 on 2021-11-22 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teleforma', '0012_merge_0011_coursetype_order_0011_merge_20210929_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursetype',
            options={'ordering': ['order'], 'verbose_name': 'course type'},
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL, unique=True, verbose_name='user'),
        ),
    ]
