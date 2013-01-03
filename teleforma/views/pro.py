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
from teleforma.context_processors import *

from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context, RequestContext
from django.views.generic.base import TemplateResponseMixin
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import escape
from django.views.generic.detail import SingleObjectMixin
from django.core.mail import EmailMessage

import os
from cgi import escape
from cStringIO import StringIO

from xhtml2pdf import pisa

from forms_builder.forms.forms import FormForForm
from forms_builder.forms.models import Form
from forms_builder.forms.signals import form_invalid, form_valid


def content_to_pdf(content, dest, encoding='utf-8', **kwargs):
    """
    Write into *dest* file object the given html *content*.
    Return True if the operation completed successfully.
    """
    from xhtml2pdf import pisa
    src = StringIO(content.encode(encoding))
    pdf = pisa.pisaDocument(src, dest, encoding=encoding, **kwargs)
    return not pdf.err

def content_to_response(content, filename=None):
    """
    Return a pdf response using given *content*.
    """
    response = HttpResponse(content, mimetype='application/pdf')
    if filename is not None:
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def render_to_pdf(request, template, context, filename=None, encoding='utf-8', 
    **kwargs):
    """
    Render a pdf response using given *request*, *template* and *context*.
    """
    if not isinstance(context, Context):
        context = RequestContext(request, context)

    content = loader.render_to_string(template, context)
    buffer = StringIO()

    succeed = content_to_pdf(content, buffer, encoding, **kwargs)
    if succeed:
        return content_to_response(buffer.getvalue(), filename)
    return HttpResponse('Errors rendering pdf:<pre>%s</pre>' % escape(content))


class SeminarView(DetailView):

    model = Seminar
    template_name='teleforma/seminar_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SeminarView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SeminarView, self).get_context_data(**kwargs)
        seminar = self.get_object()
        progress = seminar_progress(self.request.user, seminar)
        validated = seminar_validated(self.request.user, seminar)
        context['seminar_progress'] = progress
        context['seminar_validated'] = validated
        if progress == 100 and not validated:
            messages.warning(self.request, _("You have successfully terminated your e-learning seminar. A training testimonial will be available as soon as the pedagogical team validate all your answers (48h maximum)."))
        elif validated:
            messages.info(self.request, _("All your answers have been validated! You can now download the training testimonial below."))
        return context

class SeminarsView(ListView):

    model = Seminar
    template_name='teleforma/seminars.html'

    def get_queryset(self):
        return all_seminars(self.request, progress_order=True)['all_seminars']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SeminarsView, self).dispatch(*args, **kwargs)


class AnswerView(FormView):

    model = Answer
    form_class = AnswerForm
    template_name='teleforma/answer_form.html'

    def get_initial(self):
        initial = {}
        self.question = Question.objects.get(pk=self.kwargs['pk'])
        answers = Answer.objects.filter(user=self.request.user, 
                                        question=self.question).order_by('-date_submitted')
        if answers:
            answer = answers[0]
        else:
            answer = Answer()
        initial['answer'] = answer.answer
        initial['status'] = answer.status
        self.status = answer.status
        return initial

    def form_valid(self, form):
        answer = form.instance
        answer.user = self.request.user
        answer.question = self.question
        answer.save()
        if answer.status <= 2:
            messages.info(self.request, _("You have successfully saved your answer"))
        elif answer.status == 3:
            messages.info(self.request, _("You have successfully submitted your answer"))
        return super(AnswerView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AnswerView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['status'] = self.status
        context['seminar'] = self.question.seminar
        context['seminar_progress'] = seminar_progress(self.request.user, self.question.seminar)
        return context

    def get_success_url(self):
        return reverse('teleforma-seminar-detail', kwargs={'pk':self.question.seminar.id})



class MediaPackageView(DetailView):

    model = MediaPackage

    def get_context_data(self, **kwargs):
        context = super(MediaPackageView, self).get_context_data(**kwargs)
        media_package = self.get_object()
        media_package.readers.add(self.request.user)
        seminar = Seminar.objects.get(pk=self.kwargs['id'])
        context['seminar'] = seminar
        context['media_package'] = media_package
        context['seminar_progress'] = seminar_progress(self.request.user, seminar)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MediaPackageView, self).dispatch(*args, **kwargs)

    @jsonrpc_method('teleforma.publish_media_package')
    def publish(request, id):
        media_package = MediaPackage.objects.get(id=id)
        media_package.is_published = True
        media_package.save()
        for media in media_package.video.all():
            media.is_published = True
            media.save()
        for media in media_package.audio.all():
            media.is_published = True
            media.save()

    @jsonrpc_method('teleforma.unpublish_media_package')
    def unpublish(request, id):
        media_package = MediaPackage.objects.get(id=id)
        media_package.is_published = False
        media_package.save()
        for media in media_package.video.all():
            media.is_published = False
            media.save()
        for media in media_package.audio.all():
            media.is_published = False
            media.save()

                
class AnswersView(ListView):

    model = Answer
    template_name='teleforma/answers.html'

    def get_queryset(self):
        return Answer.objects.filter(status=3)

    def get_context_data(self, **kwargs):
        context = super(AnswersView, self).get_context_data(**kwargs)
        seminars = all_seminars(self.request)
        context['all_seminars'] = seminars
        
        paginator = Paginator(self.object_list, per_page=12)
        try:
            page = int(self.request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            page = paginator.page(page)
        except (InvalidPage):
            page = paginator.page(paginator.num_pages)
        context['page'] = page
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnswersView, self).dispatch(*args, **kwargs)


    @jsonrpc_method('teleforma.validate_answer')
    def validate(request, id):
        answer = Answer.objects.get(id=id)
        answer.validate()
        user = answer.user
        seminar = answer.question.seminar
        if seminar_validated(user, seminar):
            testimonial = Testimonial(user=user, seminar=seminar)
            testimonial.save()
            email = EmailMessage()
            text = 'Your training testimonial for the seminar : '
            email.subject = seminar.course.department.name + ' : ' + text + seminar.title
            name, email.from_email = settings.ADMINS[0]
            email.to = [user.email]
            email.body = 'You have validated your training!'
            email.send()


    @jsonrpc_method('teleforma.reject_answer')
    def reject(request, id):
        answer = Answer.objects.get(id=id)
        answer.validated = False
        answer.status = 2
        answer.save()


class AnswerDetailView(DetailView):

    model = Answer
    template_name='teleforma/answer_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnswerDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnswerDetailView, self).get_context_data(**kwargs)
        context['all_seminars'] = all_seminars(self.request)
        return context


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'pk': form.instance.pk,
            }
            return self.render_to_json_response(data)
        else:
            return super(AjaxableResponseMixin, self).form_valid(form)


# class EvaluationView(DetailView):

#     model = Seminar
#     template_name='teleforma/evaluation_form.html'

#     def get_context_data(self, **kwargs):
#         context = super(EvaluationView, self).get_context_data(**kwargs)
#         context['all_seminars'] = all_seminars(self.request)
#         context['total_progress'] = total_progress(self.request.user)
#         context['form'] = self.get_object().form
#         context['seminar_progress'] = seminar_progress(self.request.user, self.get_object())
#         return context


def evaluation_form_detail(request, pk, template='teleforma/evaluation_form.html'):
    """
    Display a built form and handle submission.
    """
    context = {}
    seminar = Seminar.objects.get(pk=pk)
    published = Form.objects.published(for_user=request.user)
    form = seminar.form
    if form.login_required and not request.user.is_authenticated():
        return redirect("%s?%s=%s" % (settings.LOGIN_URL, REDIRECT_FIELD_NAME,
                        urlquote(request.get_full_path())))
    request_context = RequestContext(request)
    args = (form, request_context, request.POST or None, request.FILES or None)
    form_for_form = FormForForm(*args)
    if request.method == "POST":
        if not form_for_form.is_valid():
            form_invalid.send(sender=request, form=form_for_form)
        else:
            entry = form_for_form.save()
            form_valid.send(sender=request, form=form_for_form, entry=entry)
            messages.info(request, _("You have successfully sumitted your evaluation"))
            return redirect('teleforma-seminar-detail', seminar.id)

    context['seminar'] = seminar
    context['form'] = form
    context['seminar_progress'] = seminar_progress(request.user, seminar)
    
    return render_to_response(template, context, request_context)



class PDFTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for Django class based views.
    Switch normal and pdf template based on request.

    The switch is made when the request has a particular querydict, e.g.::

        http://www.example.com?format=pdf

    The key and value of the querydict can be overridable using *as_view()*.
    That pdf url will be present in the context as *pdf_url*.

    For example it is possible to define a view like this::
        
        from django.views.generic import View

        class MyView(PDFTemplateResponseMixin, View):
            template_name = 'myapp/myview.html'
            pdf_filename = 'report.pdf'

    The pdf generation is automatically done by *xhtml2pdf* using
    the *myapp/myview_pdf.html* template.

    Note that the pdf template takes the same context as the normal template.
    """
    pdf_template_name = None
    pdf_template_name_suffix = '_pdf'
    pdf_querydict_key = 'format'
    pdf_querydict_value = 'pdf'
    pdf_encoding = 'utf-8'
    pdf_filename = None
    pdf_url_varname = 'pdf_url'
    pdf_kwargs = {}

    def is_pdf(self):
        value = self.request.REQUEST.get(self.pdf_querydict_key, '')
        return value.lower() == self.pdf_querydict_value.lower()

    def _get_pdf_template_name(self, name):
        base, ext = os.path.splitext(name)
        return '%s%s%s' % (base, self.pdf_template_name_suffix, ext)

    def get_pdf_template_names(self):
        """
        If the template name is not given using the class attribute
        *pdf_template_name*, then it is obtained using normal template
        names, appending *pdf_template_name_suffix*, e.g.::

            path/to/detail.html -> path/to/detail_pdf.html
        """
        if self.pdf_template_name is None:
            names = super(PDFTemplateResponseMixin, self).get_template_names()
            return map(self._get_pdf_template_name, names)
        return [self.pdf_template_name]

    def get_pdf_filename(self):
        """
        Return the pdf attachment filename.
        If the filename is None, the pdf will not be an attachment.
        """
        return self.pdf_filename

    def get_pdf_url(self):
        """
        This method is used to put the pdf url in the context.
        """
        querydict = self.request.GET.copy()
        querydict[self.pdf_querydict_key] = self.pdf_querydict_value
        return '%s?%s' % (self.request.path, querydict.urlencode())

    def get_pdf_response(self, context, **response_kwargs):
        return render_to_pdf(
            request=self.request, 
            template=self.get_pdf_template_names(),
            context=context, 
            encoding=self.pdf_encoding, 
            filename=self.get_pdf_filename(), 
            **self.pdf_kwargs
        )

    def render_to_response(self, context, **response_kwargs):
        if self.is_pdf():
            from django.conf import settings
            context['STATIC_ROOT'] = settings.STATIC_ROOT
            return self.get_pdf_response(context, **response_kwargs)
        context[self.pdf_url_varname] = self.get_pdf_url()
        return super(PDFTemplateResponseMixin, self).render_to_response(
            context, **response_kwargs)




class TestimonialView(PDFTemplateResponseMixin, SeminarView):

    model = Seminar
    template_name = 'teleforma/seminar_testimonial.html'
    pdf_template_name = 'teleforma/seminar_testimonial.html'
    # pdf_filename = 'report.pdf'

    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TestimonialView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TestimonialView, self).get_context_data(**kwargs)        
        context['seminar'] = self.get_object()
        return context


class TestimonialDownloadView(TestimonialView):

    pdf_filename = 'testimonial.pdf'

    def get_pdf_filename(self):
        super(TestimonialView, self).get_pdf_filename()
        seminar = self.get_object()
        prefix = unicode(_('Testimonial'))
        filename = '_'.join([prefix, seminar.title, 
                            self.request.user.first_name, self.request.user.last_name,])
        filename += '.pdf'
        return filename.encode('utf-8')

