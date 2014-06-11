# Create your views here.

from teleforma.exam.models import *
from teleforma.views.core import *


class ScriptView(CourseAccessMixin, DetailView):

    model = Script
    template_name='exam/script_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptView, self).get_context_data(**kwargs)
        script = self.get_object()
        context['script'] = script
        context['course'] = script.course

        access = get_access(script, context['all_courses'])
        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptView, self).dispatch(*args, **kwargs)


