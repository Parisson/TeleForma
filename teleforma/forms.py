
from django.forms import ModelForm
from teleforma.models import *

class ConferenceForm(ModelForm):

    class Meta:
        model = Conference


