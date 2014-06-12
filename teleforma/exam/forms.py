from django.forms import ModelForm, HiddenInput
from teleforma.exam.models import *
from django.forms.models import inlineformset_factory


class ScriptForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Script
        exclude = ['uuid', 'url', 'author', 'corrector', 'date_submitted', 'date_rejected', 'date_marked',
                ]
        #hidden_fields = ['status']
