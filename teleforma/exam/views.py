#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.

from teleforma.exam.models import *
from teleforma.exam.forms import *
from teleforma.views.core import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

import numpy as np


class ScriptMixinView(View):

    def get_context_data(self, **kwargs):
        context = super(ScriptMixinView, self).get_context_data(**kwargs)
        self.period = Period.objects.get(id=self.kwargs['period_id'])
        context['period'] = self.period
        if getattr(settings, 'TELEFORMA_EXAM_SCRIPT_UPLOAD', True) and self.period.date_exam_end:
            context['upload'] = datetime.datetime.now() <= self.period.date_exam_end
        else:
            context['upload'] = False
        return context


class ScriptView(ScriptMixinView, CourseAccessMixin, UpdateView):

    model = Script
    template_name='exam/script_detail.html'
    form_class = ScriptForm

    def get_success_url(self):
        period = Period.objects.get(id=self.kwargs['period_id'])
        return reverse_lazy('teleforma-exam-scripts-pending', kwargs={'period_id':period.id})

    def get_context_data(self, **kwargs):
        context = super(ScriptView, self).get_context_data(**kwargs)
        script = self.get_object()
        context['script'] = script
        context['course'] = script.course
        context['mark_fields'] = ['score', 'comments' ]
        context['reject_fields'] = ['reject_reason' ]

        doc_type = DocumentType.objects.get(id=settings.TELEFORMA_EXAM_TOPIC_DEFAULT_DOC_TYPE_ID)
        topics = Document.objects.filter(course=script.course, period=script.period,
                                            session=script.session, type=doc_type)
        topic = None
        if topics:
            topic = topics[0]
        context['topic'] = topic

        access = self.request.user == script.author or \
                    self.request.user == script.corrector or \
                    self.request.user.is_superuser or \
                     self.request.user.is_staff or self.request.user.professor.all()

        if not access:
            context['access_error'] = access_error
            context['message'] = contact_message

        if script.status == 4 and self.request.user == script.author:
            script.status = 5
            script.save()

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptView, self).dispatch(*args, **kwargs)


class ScriptsView(ScriptMixinView, ListView):

    model = Script
    template_name='exam/scripts.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptsView, self).dispatch(*args, **kwargs)


class ScriptsPendingView(ScriptsView):

    def get_queryset(self):
        user = self.request.user
        period = Period.objects.get(id=self.kwargs['period_id'])

        QT = Q(status=2, author=user, period=period)
        QT = Q(status=3, author=user, period=period) | QT
        QT = Q(status=3, corrector=user, period=period) | QT

        professor = user.professor.all()
        if professor:
            professor = professor[0]
            for course in professor.courses.all():
                QT = Q(status=2, period=period, course=course) | QT
                QT = Q(status=3, period=period, course=course) | QT

        return Script.objects.filter(QT)

    def get_context_data(self, **kwargs):
        context = super(ScriptsPendingView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Pending scripts')
        return context


class ScriptsTreatedView(ScriptsView):

    def get_queryset(self):
        user = self.request.user
        period = Period.objects.get(id=self.kwargs['period_id'])

        QT = Q(status=4, author=user, period=period)
        QT = Q(status=5, author=user, period=period) | QT
        QT = Q(status=4, corrector=user, period=period) | QT
        QT = Q(status=5, corrector=user, period=period) | QT

        professor = user.professor.all()
        if professor:
            professor = professor[0]
            for course in professor.courses.all():
                QT = Q(status=4, period=period, course=course) | QT
                QT = Q(status=5, period=period, course=course) | QT

        return Script.objects.filter(QT)

    def get_context_data(self, **kwargs):
        context = super(ScriptsTreatedView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Treated scripts')
        return context


class ScriptsRejectedView(ScriptsView):

    def get_queryset(self):
        user = self.request.user
        period = Period.objects.get(id=self.kwargs['period_id'])
        QT = Q(status=0, author=user)
        QT = Q(status=0, corrector=user) | QT

        professor = user.professor.all()
        if professor:
            professor = professor[0]
            for course in professor.courses.all():
                QT = Q(status=0, period=period, course=course) | QT

        return Script.objects.filter(QT)

    def get_context_data(self, **kwargs):
        context = super(ScriptsRejectedView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Rejected scripts')
        return context


class ScriptCreateView(ScriptMixinView, CreateView):

    model = Script
    template_name='exam/script_form.html'
    form_class = ScriptForm

    def get_success_url(self):
        period = Period.objects.get(id=self.kwargs['period_id'])
        return reverse_lazy('teleforma-exam-scripts-pending', kwargs={'period_id':period.id})

    def form_valid(self, form):
        period = Period.objects.get(id=self.kwargs['period_id'])
        scripts = Script.objects.filter(course=form.cleaned_data['course'], session=form.cleaned_data['session'],
                                        type=form.cleaned_data['type'], author=self.request.user, period=period).exclude(status=0)
        if scripts:
            messages.error(self.request, _("Error: you have already submitted a script for this session, the same course and the same type!"))
            return redirect('teleforma-exam-script-create', self.kwargs['period_id'])
        else:
            form.instance.author = self.request.user
            messages.info(self.request, _("You have successfully submitted your script. It will be processed in the next hours."))
        return super(ScriptCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, _("There was a problem with your submission. Please try again, later if possible."))
        return super(ScriptCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ScriptCreateView, self).get_context_data(**kwargs)
        context['create_fields'] = ['course', 'session', 'type', 'file' ]
        course_pk_list = [c['course'].id for c in get_courses(self.request.user) if c.exam_scripts]
        context['form'].fields['course'].queryset = Course.objects.filter(pk__in=course_pk_list)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptCreateView, self).dispatch(*args, **kwargs)


class ScriptUpdateView(UpdateView):

    model = Script
    fields = ['score']


class QuotasView(ListView):

    model = Quota
    template_name='exam/quotas.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuotasView, self).dispatch(*args, **kwargs)


class ScriptsScoreAllView(ScriptsTreatedView):

    template_name='exam/scores.html'

    def score_data_setup(self, x, y):
        if not x['x']:
            messages.warning(self.request, _("You must add your score to access to the statistics."))

        chartdata = x
        i = 1
        for data in y:
            chartdata['name'+str(i)] = data['name']
            chartdata['y'+str(i)] = data['data']
            i += 1
        charttype = "multiBarChart"
        chartcontainer = 'multibarchart_container'
        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,}
            }
        return data

    def get_context_data(self, **kwargs):
        context = super(ScriptsScoreAllView, self).get_context_data(**kwargs)

        if self.request.user.is_staff or self.request.user.professor.all():
            scripts = Script.objects.filter(period=self.period).exclude(score=None)
        else:
            scripts = self.get_queryset()

        sessions = []
        scores = []

        for script in scripts:
            if not script.session in sessions:
                sessions.append(script.session)
        sessions = map(str, sorted(map(int, sessions)))
        sessions_x = {'x': sessions}

        if not (self.request.user.is_staff or self.request.user.professor.all()):
            data = []
            for session in sessions:
                data.append(np.mean([float(script.score) for script in scripts.filter(session=session) if script.score]))
            scores.append({'name': 'Moyenne personnelle' + ' (' + str(len(sessions)) + ')', 'data': data})

        data = []
        counter = 0
        for session in sessions:
            scripts = Script.objects.filter(session=session, period=self.period).exclude(score=None)
            counter += scripts.count()
            data.append(np.mean([s.score for s in scripts if script.score]))
        scores.append({'name': 'Moyenne generale'  + ' (' + str(counter) + ')', 'data': data})

        for script_type in ScriptType.objects.all():
            data = []
            counter = 0
            for session in sessions:
                scripts = Script.objects.filter(session=session, period=self.period, type=script_type).exclude(score=None)
                data.append(np.mean([s.score for s in scripts if script.score]))
                counter += scripts.count()
            scores.append({'name': 'Moyenne ' + script_type.name + ' (' + str(counter) + ')', 'data': data})

        context['data'] = self.score_data_setup(sessions_x, scores)
        context['course'] = ugettext('all courses')
        return context


class ScriptsScoreCourseView(ScriptsScoreAllView):

    def get_context_data(self, **kwargs):
        context = super(ScriptsScoreCourseView, self).get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['course_id'])
        period = Period.objects.get(id=self.kwargs['period_id'])

        if self.request.user.is_staff or self.request.user.professor.all():
            scripts = Script.objects.all().filter(course=course, period=self.period).exclude(score=None)
        else:
            scripts = self.get_queryset().filter(course=course)

        sessions = []
        scores = []

        for script in scripts:
            if not script.session in sessions:
                sessions.append(script.session)
        sessions = sorted(sessions)
        sessions_x = {'x': sessions}

        if not (self.request.user.is_staff or self.request.user.professor.all()):
            data = []
            for session in sessions:
                data.append(np.mean([float(script.score) for script in scripts.filter(session=session) if script.score]))
            scores.append({'name':'Note personnelle' , 'data': data})

        data = []
        counter = 0
        for session in sessions:
            scripts = Script.objects.filter(session=session, course=course, period=self.period).exclude(score=None)
            counter += scripts.count()
            data.append(np.mean([s.score for s in scripts if script.score]))
        scores.append({'name':'Moyenne generale' + ' (' + str(counter) + ')', 'data': data})

        for script_type in ScriptType.objects.all():
            data = []
            counter = 0
            for session in sessions:
                scripts = Script.objects.filter(session=session, type=script_type, course=course, period=self.period).exclude(score=None)
                counter += scripts.count()
                data.append(np.mean([s.score for s in scripts if script.score]))
            scores.append({'name': 'Moyenne ' + script_type.name + ' (' + str(counter) + ')', 'data': data})

        context['data'] = self.score_data_setup(sessions_x, scores)
        context['course'] = course.title
        return context


class ScoreCreateView(ScriptCreateView):

    template_name='exam/score_form.html'
    form_class = ScriptForm

    def get_success_url(self):
        period = Period.objects.get(id=self.kwargs['period_id'])
        return reverse_lazy('teleforma-exam-scripts-scores-all', kwargs={'period_id':period.id})

    def get_context_data(self, **kwargs):
        context = super(ScriptCreateView, self).get_context_data(**kwargs)
        context['create_fields'] = ['course', 'session', 'type', 'score' ]
        course_pk_list = [c['course'].id for c in get_courses(self.request.user)]
        context['form'].fields['course'].queryset = Course.objects.filter(pk__in=course_pk_list)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScoreCreateView, self).dispatch(*args, **kwargs)
