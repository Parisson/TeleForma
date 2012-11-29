# -*- coding: utf-8 -*-
# Copyright (c) 2012 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Guillaume Pellerin <yomguy@parisson.com>



from teleforma.views.core import *


def get_seminars(user):
    seminars = []

    if not user.is_authenticated():
        return None

    professor = user.professor.all()
    auditor = user.auditor.all()

    if professor:
        professor = user.professor.get()
        seminars = professor.seminars.all()

    elif auditor:
        auditor = user.pro_auditor.get()
        s_seminars = auditor.seminars.all()

    elif user.is_staff or user.is_superuser:
        seminars = Seminar.objects.all()
    else:
        seminars = None

    return seminars


def seminar_progress(user, seminar):    
    """return the user progress of a seminar in percent"""

    progress = 0
    total = 0
    
    objects = [seminar.docs_1, seminar.docs_2, seminar.media, seminar.docs_correct]
    for obj in objects:
        for item in obj.all():
            total += item.weight
            if user in item.readers.all():
                progress += item.weight
    
    questions = Question.objects.filter(seminar=seminar, status=3)
    for question in questions:
        total += question.weight
        answer = Answer.objects.filter(question=question, validated=True, user=user)
        if answer:
            progress += question.weight

    return int(progress*100/total)


def total_progress(user):
    """return the user progress of all seminars in percent"""

    revisions = user.seminar_revision.all()
    progress = 0
    n = 0

    for revision in revisions:
        progress += revision.progress
        n += 1

    if n:
        return int(progress/n)
    else:
        return 0

def seminar_validated(user, seminar):
    validated = False
    for question in seminar.question.all():
        answers = question.answer.filter(user=user)
        if answers:
            validated = validated and answers[0].validated
    return validated


class SeminarView(DetailView):

    model = Seminar
    template_name='teleforma/seminar_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SeminarView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SeminarView, self).get_context_data(**kwargs)
        user = self.request.user
        seminar = self.get_object()
        context['all_seminars'] = get_seminars(user)
        context['progress'] = seminar_progress(user, seminar)
        context['total_progress'] = total_progress(user)
        context['validated'] = seminar_validated(user, seminar)
        return context


class SeminarsView(ListView):

    model = Seminar
    template_name='teleforma/seminars.html'

    def get_queryset(self):
        self.seminars = get_seminars(self.request.user)
        return self.seminars

    def get_context_data(self, **kwargs):
        context = super(SeminarsView, self).get_context_data(**kwargs)
        user = self.request.user
        context['all_seminars'] = self.seminars
        context['total_progress'] = total_progress(user)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SeminarsView, self).dispatch(*args, **kwargs)




class AnswerView(FormView):

    model = Answer
    form_class = AnswerForm
    template_name='teleforma/answer.html'


