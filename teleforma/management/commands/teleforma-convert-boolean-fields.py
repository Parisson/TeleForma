from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import django.db.models as models

class Command(BaseCommand):
    help = "Issue SQL commands to fix boolean fields after MySQL migration"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        for app, _ in apps.all_models.items():
            app_models = apps.get_app_config(app).get_models()
            for model in app_models:
                table = model._meta.db_table
                for field in model._meta.fields:
                    if isinstance(field, models.BooleanField):
                        field_name = field.column
                        print(f"alter table {table} alter {field_name} type boolean using case when {field_name}=0 then false else true end;")
