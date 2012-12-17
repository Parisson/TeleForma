
from django.forms import ModelForm, HiddenInput
from teleforma.models import *
from django.forms.models import inlineformset_factory


class ConferenceForm(ModelForm):

    class Meta:
        model = Conference


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        # exclude = ['user', 'question', 'status', 'validated', 'date_submitted']

class AnswerForm(ModelForm):

    def __init__(self, *args, **kwargs): 
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs['cols'] = 81
        self.fields['answer'].widget.attrs['rows'] = 40
        self.fields['status'].widget = HiddenInput()

    class Meta:
        model = Answer
        exclude = ['user', 'question', 'validated', 'date_submitted']
        hidden_fields = ['status']


# AnswerFormset = inlineformset_factory(QuestionForm, Answer, extra=1)

