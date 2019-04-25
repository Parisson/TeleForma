
import django.db.models as models
from django.forms import ModelForm, TextInput, Textarea
from south.modelsinspector import add_introspection_rules
from django.core.exceptions import ValidationError

try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model


class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':2, 'cols':40})}
         )
         return super(ShortTextField, self).formfield(**kwargs)

add_introspection_rules([], ["^teleforma\.fields\.ShortTextField"])



