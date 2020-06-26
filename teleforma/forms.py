
from django.forms import ModelForm, HiddenInput
from teleforma.models import *
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from teleforma.models.profile import UserProfile

class ConferenceForm(ModelForm):
    class Meta:
        model = Conference

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        # exclude = ['user', 'question', 'status', 'validated', 'date_submitted']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

class AnswerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs['cols'] = 81
        self.fields['answer'].widget.attrs['rows'] = 32
        self.fields['status'].widget = HiddenInput()
        self.fields['treated'].widget = HiddenInput()

    class Meta:
        model = Answer
        exclude = ['user', 'question', 'validated', 'date_submitted', 'date_validated']
        hidden_fields = ['status']
