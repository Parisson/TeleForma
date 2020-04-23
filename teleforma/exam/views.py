#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.

from teleforma.exam.models import *
from teleforma.exam.forms import *
from teleforma.views.core import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
import json
import numpy as np

from django.contrib.auth.decorators import permission_required
from django.db.models import Q

STUDENT = 0
CORRECTOR = 1
PROFESSOR = 2


class ScriptMixinView(View):

    def get_course_pk_list(self):
        """
        Get the list of pk of courses current user is allowed to access
        """
        courses = [ c['course'] for c in get_courses(self.request.user) ]
        courses = [ c for c in courses if c.has_exam_scripts ]
        courses = [ c for c in courses if c.is_for_period(self.period) ]
        return [ c.id for c in courses ]
        
    def get_context_data(self, **kwargs):
        context = super(ScriptMixinView, self).get_context_data(**kwargs)
        self.period = Period.objects.get(id=self.kwargs['period_id'])
        context['period'] = self.period
        course_pk_list = self.get_course_pk_list()
        context['courses'] = Course.objects.filter(pk__in=course_pk_list)
        context['script_service_url'] = getattr(settings, 'TELEFORMA_EXAM_SCRIPT_SERVICE_URL')
        self.nb_script = self.period.nb_script or settings.TELEFORMA_EXAM_MAX_SESSIONS
        if getattr(settings, 'TELEFORMA_EXAM_SCRIPT_UPLOAD', True) and self.period.date_exam_end:
            upload = datetime.datetime.now() <= self.period.date_exam_end
            cur_scripts = Script.objects.filter(period = self.period,
                                                author = self.request.user)\
                                        .exclude(status=0).count()
            allowed_scripts = self.nb_script * len(self.get_course_pk_list())
            if cur_scripts >= allowed_scripts:
                upload = False
            context['upload'] = upload
        else:
            context['upload'] = False

        context['admin'] = self.request.user.is_superuser

        return context

class ScriptsListMixinView(ScriptMixinView):

    def get_profile(self):
        user = self.request.user
        professor = user.professor.all()
        if user.is_superuser:
            return PROFESSOR
        if professor:
            return PROFESSOR
        if user.quotas.all():
            return CORRECTOR
        return STUDENT

    def get_context_data(self, **kwargs):
        context = super(ScriptsListMixinView, self).get_context_data(**kwargs)
        context['profile'] = self.get_profile()

        if context['profile'] >= CORRECTOR:
            correctors = User.objects.filter(corrector_scripts__in=self.get_base_queryset()).order_by('last_name').distinct()
            context['correctors_list'] = [(str(corrector.id), corrector.get_full_name()) for corrector in correctors]
            context['corrector_selected'] = self.request.GET.get('corrector', str(self.request.user.id))
            session_choices = get_n_choices(self.nb_script + 1)
            context['sessions_list'] = session_choices
            context['session_selected'] = self.request.GET.get('session')
            types = ScriptType.objects.all()
            context['types_list'] = [(str(type.id), type.name) for type in types]
            context['type_selected'] = self.request.GET.get('type')
            courses = Course.objects.filter(scripts__in=self.get_base_queryset()).distinct()
            context['courses_list'] = [(str(course.id), course.title) for course in courses]
            context['course_selected'] = self.request.GET.get('course')
            context['platform_only'] = self.request.GET.get('platform_only')
        return context

class ScriptView(ScriptMixinView, CourseAccessMixin, UpdateView):

    model = Script
    template_name='exam/script_detail.html'
    form_class = ScriptForm

    def get_form_kwargs(self):
        kwargs = super(ScriptView, self).get_form_kwargs()
        script = self.get_object()
        kwargs['period'] = script.period
        return kwargs

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
        topics = Document.objects.filter(course=script.course, periods__in=(script.period,),
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


class ScriptsView(ScriptsListMixinView, ListView):

    model = Script
    template_name='exam/scripts.html'
    status_filter = None

    def get_form_queryset(self):
        QT = ~Q(pk=None)
        corrector = self.request.GET.get('corrector')
        type = self.request.GET.get('type')
        session = self.request.GET.get('session')
        course = self.request.GET.get('course')
        platform_only = self.request.GET.get('platform_only')
        if type:
            QT &= Q(type__id=int(type))
        if session:
            QT &= Q(session=session)
        if course:
            QT &= Q(course__id=int(course))
        if corrector:
            QT &= Q(corrector__id=int(corrector))
        if platform_only:
            QT &= Q(author__student__platform_only = int(platform_only))
        return QT
 
    def get_base_queryset(self):
        QT = self.get_form_queryset() & Q(period_id=self.kwargs['period_id'])
        if self.status_filter:
            QT &= Q(status__in=self.status_filter)
        return Script.objects.filter(QT)

    def get_queryset(self):
        user = self.request.user
        base_qs = self.get_base_queryset()

        if self.request.GET.get('corrector') is None:
            QT = Q(author=user) | Q(corrector=user)

            professor = user.professor.all()
            if professor:
                professor = professor[0]
                courses_id = [ c['id'] for c in professor.courses.values('id') ]
                QT |= Q(course_id__in=courses_id)

            base_qs = base_qs.filter(QT)

        if self.get_profile() == STUDENT:
            base_qs = base_qs.order_by('-date_submitted')
        return base_qs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScriptsView, self).dispatch(*args, **kwargs)


class ScriptsPendingView(ScriptsView):

    status_filter = (2, 3)

    def get_queryset(self):
        qs = super(ScriptsPendingView, self).get_queryset()
        
        if self.request.GET.get('corrector') is None:
            user = self.request.user
            # Exclude status=2 but not author=user
            qs = qs.filter(~Q(status=2) | Q(author=user))

        return qs

    def get_context_data(self, **kwargs):
        context = super(ScriptsPendingView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Pending scripts')
        return context


class ScriptsTreatedView(ScriptsView):

    status_filter = (4, 5 ,7)
    
    def get_context_data(self, **kwargs):
        context = super(ScriptsTreatedView, self).get_context_data(**kwargs)
        period = Period.objects.get(id=self.kwargs['period_id'])
        context['title'] = ugettext('Treated scripts')
        return context


class ScriptsRejectedView(ScriptsView):
    status_filter = (0,)

    def get_context_data(self, **kwargs):
        context = super(ScriptsRejectedView, self).get_context_data(**kwargs)
        context['title'] = ugettext('Rejected scripts')
        return context


class ScriptCreateView(ScriptMixinView, CreateView):

    model = Script
    template_name='exam/script_form.html'
    form_class = ScriptForm

    def get_success_url(self):
        return reverse_lazy('teleforma-exam-scripts-pending', kwargs={'period_id':self.period.id})

    def form_valid(self, form):
        scripts = Script.objects.filter(course=form.cleaned_data['course'], session=form.cleaned_data['session'],
                                        type=form.cleaned_data['type'], author=self.request.user, period=self.period).exclude(status=0)
        if scripts:
            messages.error(self.request, _("Error: you have already submitted a script for this session, the same course and the same type!"))
            return redirect('teleforma-exam-script-create', self.period.id)
        else:
            form.instance.author = self.request.user
            messages.info(self.request, _("You have successfully submitted your script. It will be processed in the next hours."))
        return super(ScriptCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("There was a problem with your submission. Please try again, later if possible."))
        return super(ScriptCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):    
        context = super(ScriptCreateView, self).get_context_data(**kwargs)
        context['create_fields'] = ['course', 'session', 'type', 'file' ]
        context['form'].fields['course'].queryset = context['courses']
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.period = Period.objects.get(id=kwargs['period_id'])
        return super(ScriptCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ScriptCreateView, self).get_form_kwargs()
        kwargs['period'] = self.period
        return kwargs



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

    perso_name = 'Moyenne personnelle'
    
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
                'chart_attr': { 'reduceXTicks': 0 },
                'tag_script_js': True,
                'jquery_on_ready': False,}
            }
        return data

    def get_context_data(self, **kwargs):
        context = super(ScriptsScoreAllView, self).get_context_data(**kwargs)
        user = self.request.user
        period_id = self.kwargs['period_id']
        
        if 'course_id' in self.kwargs:
            course = Course.objects.get(id=self.kwargs['course_id'])
        else:
            course = None

        is_staff = user.is_staff
        staff_or_teacher = is_staff or user.professor.exists()

        QT = Q(period_id=period_id, status__in = self.status_filter)
        all_scripts = Script.objects.filter(QT).exclude(score=None)

        if is_staff:
            QT |= Q(date_added__gte=self.period.date_begin)
            scripts = Script.objects.filter(QT).exclude(score=None)
        else:
            scripts = self.get_queryset()

        if course:
            scripts = scripts.filter(course=course)
            all_scripts = all_scripts.filter(course=course)
            
        sessions = set()
        scores = []

        for script in scripts.values('session'):
            sessions.add(script['session'])
        sessions = sorted(sessions, key = lambda v: int(v))
        sessions_x = {'x': sessions}

        def by_session(scripts):
            res = { s: [] for s in sessions }
            for script in scripts.values('score', 'session'):
                if script['session'] in res:
                    res[script['session']].append(script['score'])
            return [ np.mean(res[s]) for s in sessions ]
        
        if not staff_or_teacher:
            scores.append({'name': self.perso_name,
                           'data': by_session(scripts)})
            
        scores.append({'name': 'Moyenne generale',
                       'data': by_session(all_scripts)})

        for script_type in ScriptType.objects.all():
            scripts = all_scripts.filter(type=script_type)
            scores.append({'name': 'Moyenne ' + script_type.name, 
                           'data': by_session(scripts)})

        context['data'] = self.score_data_setup(sessions_x, scores)
        context['course'] = course and course.title or ugettext('all courses')
        return context


class ScriptsScoreCourseView(ScriptsScoreAllView):
    perso_name = 'Note personnelle'


class ScoreCreateView(ScriptCreateView):

    template_name='exam/score_form.html'
    form_class = ScoreForm

    def form_invalid(self, form):
        messages.error(self.request, "Il y une erreur sur ce formulaire, veuillez le corriger.")
        return super(ScriptCreateView, self).form_invalid(form)

    def get_success_url(self):
        period = Period.objects.get(id=self.kwargs['period_id'])
        return reverse_lazy('teleforma-exam-scripts-scores-all', kwargs={'period_id':period.id})

    def get_context_data(self, **kwargs):
        context = super(ScoreCreateView, self).get_context_data(**kwargs)
        context['create_fields'] = ['course', 'session', 'type', 'score' ]
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScoreCreateView, self).dispatch(*args, **kwargs)


def get_correctors(request):
    period = request.GET.get('period')
    course = request.GET.get('course')

    correctors = []
    for corrector in User.objects.filter(quotas__period__id = period, quotas__course__id = course).order_by('last_name').distinct():
        correctors.append({'label': '%s %s' % (corrector.last_name, corrector.first_name), 'value':corrector.id})
    dump = json.dumps(correctors)
    return HttpResponse(dump, content_type='application/json')

class MassScoreCreateView(ScoreCreateView):

    template_name='exam/mass_score_form.html'
    form_class = MassScoreForm

    def get_allowed_students(self, course_id, session):
        """
        Get allowed students for given course and session
        """
        students = Student.objects.filter(period = self.period)

        # Exclude students who already have a script for this session
        scripts = Script.objects.filter(period = self.period,
                                        session = session,
                                        course_id = course_id).values('author_id')
        scripts = set([s['author_id'] for s in scripts])
        
        students = students.exclude(user_id__in = scripts)            

        res = []
        for student in students:
           user = student.user
           # FIXME : Filter those who access the course, but that's very slow,
           # so I disable it for now - we'll see if we can do that faster later    
           # courses = get_courses(user)
           # if course_id in [ c['course'].id for c in courses ]:
           res.append({ 'id': user.id,
                        'name': str(user) })
        
        return res

    def form_valid(self, form):
        course = form.cleaned_data['course']
        session = form.cleaned_data['session']
        sc_type = form.cleaned_data['type']

        allowed_students = self.get_allowed_students(course.id,
                                                     session)
        allowed_students = set([ str(s['id']) for s in allowed_students ])
        done = set()
        nb_errors = 0
        nb_ok = 0

        for student, score in form.cleaned_data['scores']:
            if student in done:
                nb_errors += 1
                continue
            if not student in allowed_students:
                nb_errors += 1
                continue
            nb_ok += 1
            done.add(student)
            obj = Script(course = course,
                         period = self.period,
                         session = session,
                         author_id = student,
                         type = sc_type,
                         score = score,                                 
                         status = 7)
            obj.save()

        messages.info(self.request, "%d notes créées, %d en erreur (copie déjà existante, ...)" % (nb_ok, nb_errors))

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MassScoreCreateView, self).get_context_data(**kwargs)
        context['create_fields'] = ['course', 'session', 'type' ]
        context['rows'] = [ { 'student_name': 'student%d' % i,
                              'score_name': 'score%d' % i } for i in range(20) ]
        for row in context['rows']:
            student = self.request.POST.get(row['student_name'], '')
            label = ""
            if student:
                user = User.objects.get(pk=student)
                label = "%s %s - %s" % (user.last_name, user.first_name, user.username)
            row['student_value'] = self.request.POST.get(row['student_name'], '')
            row['student_label'] = label
            row['score_value'] = self.request.POST.get(row['score_name'], '')
            row['error'] = context['form'].table_errors.get(row['student_name'], None)
        return context

    @method_decorator(permission_required('is_superuser'))
    def dispatch(self, *args, **kwargs):
        return super(ScoreCreateView, self).dispatch(*args, **kwargs)


def get_mass_students(request):
    """
    Get allowed students for given course and session
    """
    period = request.GET.get('period')
    session = request.GET.get('session')
    course_id = request.GET.get('course_id')
    q = request.GET.get('q[term]')
    # import pdb;pdb.set_trace()
    students = Student.objects.filter(period = period).filter(Q(user__username__icontains=q) | Q(user__last_name__icontains=q) | Q(user__first_name__icontains=q))

    # Exclude students who already have a script for this session
    scripts = Script.objects.filter(period = period,
                                    session = session,
                                    course_id = course_id).values('author_id')
    scripts = set([s['author_id'] for s in scripts])

    students = students.exclude(user_id__in = scripts)

    res = []
    for student in students:
       user = student.user
       # FIXME : Filter those who access the course, but that's very slow,
       # so I disable it for now - we'll see if we can do that faster later
       # courses = get_courses(user)
       # if course_id in [ c['course'].id for c in courses ]:
       res.append({ 'id': user.id,
                    'text': "%s %s - %s" % (user.last_name, user.first_name, user.username) })

    data = {'results':res, 'pagination':{'more':False}}
    return HttpResponse(json.dumps(data), content_type='application/json')
