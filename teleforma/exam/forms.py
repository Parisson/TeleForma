from django.forms import ModelForm, HiddenInput
from teleforma.exam.models import *
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

def validate_session(nb):
    def validator(value):
        if int(value) > nb:
            raise ValidationError(u'session invalide: %s' % value)
    return validator

class ScriptForm(ModelForm):

    def __init__(self, *args, **kwargs):
        period = kwargs.pop('period')
        super(ScriptForm, self).__init__(*args, **kwargs)
        self.fields['score'].localize = True
        nb = period.nb_script or settings.TELEFORMA_EXAM_MAX_SESSIONS
        self.fields['session'] = forms.ChoiceField(choices = get_n_choices(nb + 1),
                                                   validators = [ validate_session(nb) ])

    class Meta:
        model = Script
        exclude = ['uuid', 'mime_type', 'sha1', 'url',
                    'date_submitted', 'date_rejected', 'date_marked',
                    'box_uuid',]
        #hidden_fields = ['status']


class ScoreForm(ScriptForm):
    pass
