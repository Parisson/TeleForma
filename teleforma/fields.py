
import django.db.models as models
from south.modelsinspector import add_introspection_rules

class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':3, 'cols':30})}
         )
         return super(ShortTextField, self).formfield(**kwargs)

add_introspection_rules([], ["^teleforma\.models\.ShortTextField"])

