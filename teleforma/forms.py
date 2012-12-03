
from django.forms import ModelForm
from teleforma.models import *
from django.forms.models import inlineformset_factory


class ConferenceForm(ModelForm):

    class Meta:
        model = Conference


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        # exclude = ['user', 'question', 'status', 'validated', 'date_submitted']


AnswerFormset = inlineformset_factory(QuestionForm, Answer, extra=1)

