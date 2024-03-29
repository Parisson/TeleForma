from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ..exam.models import Script
from ..models.core import get_n_choices


def validate_session(nb):
    def validator(value):
        if int(value) > nb:
            raise ValidationError(u'session invalide: %s' % value)
    return validator


class ScriptForm(ModelForm):

    def __init__(self, *args, **kwargs):
        period = kwargs.pop('period')
        super(ScriptForm, self).__init__(*args, **kwargs)
        self.fields['score'].localize = False
        nb = period.nb_script or settings.TELEFORMA_EXAM_MAX_SESSIONS
        self.fields['session'] = forms.ChoiceField(choices=get_n_choices(nb + 1),
                                                   validators=[validate_session(nb)])
        self.fields['file'].required = True
        self.fields['score'].widget.attrs['onkeydown'] = "return event.key != 'Enter';"

    class Meta:
        model = Script
        exclude = ['uuid', 'mime_type', 'sha1', 'url', 'type'
                   'date_submitted', 'date_rejected', 'date_marked',
                   'box_uuid', ]
        #hidden_fields = ['status']


class ScoreForm(ScriptForm):
    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['score'].required = True


class MassScoreForm(ScoreForm):

    def __init__(self, *args, **kwargs):
        super(MassScoreForm, self).__init__(*args, **kwargs)
        self.table_errors = {}
        self.fields['score'].required = False

    def clean(self):
        cleaned_data = super(MassScoreForm, self).clean()

        errors = {}
        valid = []

        for key in self.data.keys():
            if key.startswith('student'):
                student = self.data[key]
                if student:
                    score = self.data[key.replace('student', 'score')]
                    try:
                        score = float(score.replace(',', '.'))
                    except ValueError:
                        errors[key] = u"Note invalide"
                        continue
                    valid.append((student, score))

        cleaned_data['scores'] = valid
        self.table_errors = errors

        if errors:
            raise forms.ValidationError("Certaines notes sont invalides")
        return cleaned_data
