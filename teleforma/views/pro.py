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


from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from ..decorators import access_required
from ..models.pro import Answer, Question, Seminar


class SeminarView(DetailView):

    model = Seminar
    template_name = 'teleforma/seminar_detail.html'

    @method_decorator(access_required)
    def dispatch(self, *args, **kwargs):
        return super(SeminarView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SeminarView, self).get_context_data(**kwargs)
        user = self.request.user
        seminar = self.get_object()
        context['seminars'] = Seminar.objects.filter(suscribers__in=user)
        context['progress'] = self.progress(user, seminar)
        return context

    def progress(user, seminar):
        """return the user progress of a seminar in percent"""

        progress = 0
        total = 0

        docs = [seminar.doc_1, seminar.doc_2,
                seminar.media, seminar.doc_correct]
        for doc in docs:
            total += doc.weight
            if user in doc.readers:
                progress += doc.weight

        questions = Question.objects.filter(seminar=seminar, status=3)
        for question in questions:
            total += question.weight
            answer = Answer.objects.filter(
                question=question, validated=True, user=user)
            if answer:
                progress += question.weight

        return int(progress*100/total)
