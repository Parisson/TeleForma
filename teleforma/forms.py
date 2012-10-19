
from django.forms import ModelForm
from teleforma.models import *

class ConferenceForm(ModelForm):

    class Meta:
        model = Conference

class SeminarForm(ModelForm):

    class Meta:
        model = Seminar

class AnswerForm(ModelForm):

    class Meta:
        model = Answer



