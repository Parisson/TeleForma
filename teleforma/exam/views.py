# Create your views here.

from teleforma.exam.models import *
from teleforma.views.core import *


class ScriptView(DetailView):

    model = Script
    template_name='exam/script_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptView, self).get_context_data(**kwargs)
        script = self.get_object()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConferenceView, self).dispatch(*args, **kwargs)

