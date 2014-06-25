# Create your views here.

from teleforma.exam.models import *
from teleforma.exam.forms import *
from teleforma.views.core import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse


class ScriptView(CourseAccessMixin, UpdateView):

    model = Script
    template_name='exam/script_detail.html'
    form_class = ScriptForm
    success_url = reverse_lazy('teleforma-exam-scripts-pending', kwargs={'period_id':1})

    def get_context_data(self, **kwargs):
        context = super(ScriptView, self).get_context_data(**kwargs)
        script = self.get_object()
        context['script'] = script
        context['course'] = script.course
        context['mark_fields'] = ['score', 'comments' ]
        context['reject_fields'] = ['reject_reason' ]

        doc_type = DocumentType.objects.get(number=settings.TELEFORMA_EXAM_TOPIC_DEFAULT_DOC_TYPE_NUMBER)
        topics = Document.objects.filter(course=script.course, period=script.period,
                                            session=script.session, type=doc_type)
        topic = None
        if topics:
            topic = topics[0]
        context['topic'] = topic

        access = self.request.user == script.author or \
                    self.request.user == script.corrector or \
                    self.request.user.is_superuser or \
                     self.request.user.is_staff

        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptView, self).dispatch(*args, **kwargs)


class ScriptsView(ListView):

    model = Script
    template_name='exam/scripts.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptsView, self).get_context_data(**kwargs)
        context['period'] = Period.objects.get(id=self.kwargs['period_id'])
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptsView, self).dispatch(*args, **kwargs)


class ScriptsPendingView(ScriptsView):

    def get_queryset(self):
        user = self.request.user
        scripts = Script.objects.filter(Q(status=3, author=user) | Q(status=3, corrector=user))
        return scripts

    def get_context_data(self, **kwargs):
        context = super(ScriptsPendingView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Pending scripts')
        return context


class ScriptsTreatedView(ScriptsView):

    def get_queryset(self):
        user = self.request.user
        scripts = Script.objects.filter(Q(status=4, author=user) | Q(status=4, corrector=user))
        return scripts

    def get_context_data(self, **kwargs):
        context = super(ScriptsTreatedView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Treated scripts')
        return context


class ScriptsRejectedView(ScriptsView):

    def get_queryset(self):
        user = self.request.user
        scripts = Script.objects.filter(Q(status=0, author=user) | Q(status=0, corrector=user))
        return scripts

    def get_context_data(self, **kwargs):
        context = super(ScriptsRejectedView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Rejected scripts')
        return context


class ScriptCreateView(CreateView):

    model = Script
    template_name='exam/script_form.html'
    form_class = ScriptForm
    success_url = reverse_lazy('teleforma-exam-scripts-pending', kwargs={'period_id':1})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ScriptCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ScriptCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ScriptCreateView, self).get_context_data(**kwargs)
        context['period'] = Period.objects.get(id=self.kwargs['period_id'])
        context['create_fields'] = ['course', 'session', 'type', 'file' ]
        course_pk_list = [c['course'].id for c in get_courses(self.request.user)]
        context['form'].fields['course'].queryset = Course.objects.filter(pk__in=course_pk_list)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptCreateView, self).dispatch(*args, **kwargs)


class ScriptUpdateView(UpdateView):

    model = Script
    fields = ['score']

