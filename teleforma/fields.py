
import django.db.models as models
from django.forms import ModelForm, TextInput, Textarea
from south.modelsinspector import add_introspection_rules
from postman.fields import BasicCommaSeparatedUserField as PostmanBasicCommaSeparatedUserField
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



class BasicCommaSeparatedUserField(PostmanBasicCommaSeparatedUserField):
    def clean(self, value):
        """Check names are valid and filter them."""
        names = super(PostmanBasicCommaSeparatedUserField, self).clean(value)
        if not names:
            return []
        user_model = get_user_model()
        users = list(user_model.objects.filter(is_active=True, **{'{0}__in'.format(user_model.USERNAME_FIELD): names}))
        unknown_names = set(names) ^ set([u.get_username() for u in users])
        errors = []

        if unknown_names == set(['auto']):
            return unknown_names

        if unknown_names:
            errors.append(self.error_messages['unknown'].format(users=', '.join(unknown_names)))

        if self.user_filter:
            filtered_names = []
            for u in users[:]:
                try:
                    reason = self.user_filter(u)
                    if reason is not None:
                        users.remove(u)
                        filtered_names.append(
                            self.error_messages[
                                'filtered_user_with_reason' if reason else 'filtered_user'
                            ].format(username=u.get_username(), reason=reason)
                        )
                except ValidationError as e:
                    users.remove(u)
                    errors.extend(e.messages)
            if filtered_names:
                errors.append(self.error_messages['filtered'].format(users=', '.join(filtered_names)))
        if errors:
            raise ValidationError(errors)
        return users