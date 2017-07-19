from django.forms import ModelForm, HiddenInput
from teleforma.exam.models import *
from django.forms.models import inlineformset_factory


class ScriptForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)
        self.fields['score'].localize = True

    class Meta:
        model = Script
        exclude = ['uuid', 'mime_type', 'sha1', 'url',
                    'date_submitted', 'date_rejected', 'date_marked',
                    'box_uuid',]
        #hidden_fields = ['status']


class ScoreForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)
        self.fields['score'].localize = True

    class Meta:
        model = Script
        exclude = ['uuid', 'mime_type', 'sha1', 'url',
                    'date_submitted', 'date_rejected', 'date_marked',
                    'box_uuid', file]
