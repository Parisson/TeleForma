# -*- coding: utf-8 -*-
# Copyright (c) 2007-2012 Parisson SARL

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

import os.path

from django.conf.urls import include
from django.urls import re_path
from django.conf import settings
from django.urls import path
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordContextMixin,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView)
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from jsonrpc import jsonrpc_site

from teleforma.views.home import HomeView
from teleforma.views.password import TFPasswordResetConfirmView, TFPasswordResetView

from .views.appointment import Appointments, cancel_appointment
from .views.core import (ChatMessageView, ConferenceListView, ConferenceView, CourseListView,
                         CoursePendingListView, CourseView, DocumentView,
                         HelpView, HomeRedirectView, LiveConferenceNotify, MediaTranscodedView,
                         MediaView, MediaViewEmbed, NotificationView)
from .views.crfpa import (AnnalsCourseView, AnnalsIEJView, AnnalsView,
                          CorrectorAddView, CorrectorCompleteView,
                          CorrectorRegistrationPDFView,
                          CorrectorRegistrationPDFViewDownload,
                          CRFPAProfileView, NewsItemCreate, NewsItemDelete,
                          NewsItemList, NewsItemUpdate, ReceiptPDFView,
                          ReceiptPDFViewDownload, RegistrationPDFView,
                          RegistrationPDFViewDownload, RetractationView, UserAddView,
                          UserCompleteView, UserLoginView, UsersExportView,
                          UsersView, WriteView, update_training,
                          UserAddUseYourLawOriginView, QuizQuestionView)
from .views.payment import (PaymentStartView, bank_auto, bank_cancel,
                            bank_fail, bank_success)


htdocs_forma = os.path.dirname(__file__) + '/static/teleforma/'
profile_view = CRFPAProfileView()
document = DocumentView()
media = MediaView()
home_view = HomeView()
media_transcoded = MediaTranscodedView()


urlpatterns = [
    # login / logout
    re_path(r'^login/$', LoginView.as_view(template_name='teleforma/login.html'),
        name="telemeta-login"),
    re_path(r'^accounts/login/$', LoginView.as_view(template_name='teleforma/login.html'),
        name="teleforma-login"),
    re_path(r'^logout/$', LogoutView.as_view(),
        name="teleforma-logout"),

    # (r'^accounts/register0/$', RegistrationView.as_view(), {'form_class':CustomRegistrationForm}),
    re_path(r'^accounts/register/$', UserAddView.as_view(),
        name="teleforma-register"),
    re_path(r'^accounts/register/uyl/$', UserAddUseYourLawOriginView.as_view(),
        name="teleforma-register-uyl"),
    re_path(r'^accounts/register/(?P<username>.*)/complete/$',
        UserCompleteView.as_view(), name="teleforma-register-complete"),
    re_path(r'^accounts/register/(?P<username>.*)/download/$',
        RegistrationPDFViewDownload.as_view(), name="teleforma-registration-download"),
    re_path(r'^accounts/register/(?P<username>.*)/view/$',
        RegistrationPDFView.as_view(), name="teleforma-registration-view"),

    re_path(r'^correctors/register/$', CorrectorAddView.as_view(),
        name="teleforma-corrector-register"),
    re_path(r'^correctors/register/(?P<username>.*)/complete/$',
        CorrectorCompleteView.as_view(), name="teleforma-corrector-register-complete"),
    re_path(r'^correctors/register/(?P<username>.*)/download/$',
        CorrectorRegistrationPDFViewDownload.as_view(), name="teleforma-corrector-registration-download"),
    re_path(r'^correctors/register/(?P<username>.*)/view/$',
        CorrectorRegistrationPDFView.as_view(), name="teleforma-corrector-registration-view"),

    re_path(r'^users/(?P<username>[A-Za-z0-9+@._-]+)/profile/$', profile_view.profile_detail,
        name="teleforma-profile-detail"),
    re_path(r'^accounts/(?P<username>[A-Za-z0-9+@._-]+)/profile/$',
        profile_view.profile_detail, name="teleforma-profile-detail"),
    re_path(r'^accounts/(?P<username>[A-Za-z0-9+@._-]+)/profile/edit/$',
        profile_view.profile_edit, name="teleforma-profile-edit"),

    # Registration
    re_path(r'^accounts/password_change/$', PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
        name="teleforma-password-change"),
    re_path(r'^accounts/password_change_done/$', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name="password_change_done"),

    re_path(r'^accounts/password_reset/$', TFPasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                                                 email_template_name='registration/password_reset_email.html'), name="teleforma-password-reset"),
    re_path(r'^accounts/password_reset_done/$', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', TFPasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name="teleforma-password-reset-confirm"),
    re_path(r'^accounts/password_reset_complete/$', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name="password_reset_complete"),

    # Help
    re_path(r'^help/$', HelpView.as_view(), name="teleforma-help"),

    # Home
    re_path(r'^$', HomeRedirectView.as_view(),
        name="teleforma-home"),

    # Flat pages
    re_path(r'^pages/(?P<path>.*)$', home_view.render_flatpage,
        name="teleforma-flatpage"),
    # Unauthorized
    re_path(r'^unauthorized/$', TemplateView.as_view(template_name="teleforma/unauthorized.html"),
        name="teleforma-unauthorized"),


    # Desk
    re_path(r'^desk/$', HomeRedirectView.as_view(),
        name="teleforma-desk"),
    re_path(r'^desk/periods/(?P<period_id>.*)/courses/$',
        CourseListView.as_view(), name="teleforma-desk-period-list"),
    re_path(r'^desk/periods/(?P<period_id>.*)/courses_pending/$',
        CoursePendingListView.as_view(), name="teleforma-desk-period-pending"),
    re_path(r'^desk/periods/(?P<period_id>.*)/courses/(?P<pk>.*)/detail/$', 
        CourseView.as_view(),
        name="teleforma-desk-period-course"),
    re_path(r'^desk/periods/(?P<period_id>.*)/courses/(?P<pk>.*)/retractation/$', 
        RetractationView.as_view(),
        name="teleforma-desk-period-course-retractation"),

    # Media
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/transcode/(?P<pk>.*)/detail/$',
        MediaTranscodedView.as_view(), name="teleforma-media-transcoded"),
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/transcode/(?P<pk>.*)/download/$',
        media_transcoded.download, name="teleforma-media-transcoded-download"),
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/transcode/(?P<pk>.*)/stream/$',
        media_transcoded.stream, name="teleforma-media-transcoded-stream"),
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/detail/$',
        MediaView.as_view(),
        name="teleforma-media-detail"),
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/embed/$',
        MediaViewEmbed.as_view(), name="teleforma-media-embed"),
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/download/$',
        media.download, name="teleforma-media-download"),
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/stream/$',
        media.stream, name="teleforma-media-stream"),

    # Documents
    re_path(r'^desk/documents/(?P<pk>.*)/detail/$', DocumentView.as_view(),
        name="teleforma-document-detail"),
    re_path(r'^desk/documents/(?P<pk>.*)/download/$', document.download,
        name="teleforma-document-download"),
    re_path(r'^desk/documents/(?P<pk>.*)/view/$', document.view,
        name="teleforma-document-view"),

    # Annals
    re_path(r'^archives/annals/$', 
        AnnalsView.as_view(),
        name="teleforma-annals"),
    re_path(r'^archives/annals/by-iej/(\w+)/$',
        AnnalsIEJView.as_view(), name="teleforma-annals-iej"),
    re_path(r'^archives/annals/by-course/(\w+)/$',
        AnnalsCourseView.as_view(), name="teleforma-annals-course"),

    # Conferences
    re_path(r'^desk/periods/(?P<period_id>.*)/conferences/(?P<pk>.*)/video/$',
        ConferenceView.as_view(),
        name="teleforma-conference-detail"),
    re_path(r'^desk/periods/(?P<period_id>.*)/conferences/(?P<pk>.*)/audio/$',
        ConferenceView.as_view(
            template_name="teleforma/course_conference_audio.html"),
        name="teleforma-conference-audio"),
    re_path(r'^desk/periods/(?P<period_id>.*)/conferences/list/$', ConferenceListView.as_view(),
        name="teleforma-conferences"),

    # APPOINTMENTS
    re_path(r'^desk/periods/(?P<period_id>.*)/appointments/(?P<course_id>.*)/$', Appointments.as_view(),
        name="teleforma-appointments"),
    re_path(r'^desk/periods/appointments/cancel$', cancel_appointment,
        name="teleforma-appointment-cancel"),

    # Postman
    re_path(r'^messages/write/(?:(?P<recipients>[^/#]+)/)?$',
        WriteView.as_view(), name='postman:write'),
    re_path(r'^messages/', include('postman.urls')),


    # Users
    re_path(r'^users/training/(?P<training_id>.*)/iej/(?P<iej_id>.*)/course/(?P<course_id>.*)/list/$',
        UsersView.as_view(), name="teleforma-users"),

    re_path(r'^users/training/(?P<training_id>.*)/iej/(?P<iej_id>.*)/course/(?P<course_id>.*)/export/$',
        UsersExportView.as_view(), name="teleforma-users-export"),

    re_path(r'^users/(?P<id>.*)/login/$',
        UserLoginView.as_view(), name="teleforma-user-login"),

    # Ajax update training
    re_path(r'^update-training/(?P<id>.*)/$',
        update_training, name="update-training"),

    # News Item
    re_path(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/detail/$',
        MediaView.as_view(), name="teleforma-media-detail"),
    re_path(r'^newsitems/create', NewsItemCreate.as_view(),
        name='newsitem-create'),
    re_path(r'^newsitems/update/(?P<pk>.*)',
        NewsItemUpdate.as_view(), name='newsitem-update'),
    re_path(r'^newsitems/delete/(?P<pk>.*)',
        NewsItemDelete.as_view(), name='newsitem-delete'),
    re_path(r'^newsitems/(?P<period_id>.*)/list',
        NewsItemList.as_view(), name='newsitem-list'),

    # JSON RPC
    re_path(r'json/$', jsonrpc_site.dispatch,
        name='jsonrpc_mountpoint'),
    re_path(r'jsonrpc/$', jsonrpc_site.dispatch,
        name='jsonrpc_mountpoint'),

    #    re_path(r'^private_files/', include('private_files.urls')),

    # EXAM
    re_path(r'^', include('teleforma.exam.urls')),

    # WEBCLASS
    re_path(r'^', include('teleforma.webclass.urls')),

    # Payment
    re_path(r'^payment/(?P<pk>.*)/start/$', PaymentStartView.as_view(),
        name="teleforma-payment-start"),

    re_path(r'^payment/bank_auto/(?P<merchant_id>.*)',
        bank_auto, name='teleforma-bank-auto'),
    re_path(r'^payment/bank_success/(?P<merchant_id>.*)',
        bank_success, name='teleforma-bank-success'),
    re_path(r'^payment/bank_cancel/(?P<merchant_id>.*)',
        bank_cancel, name='teleforma-bank-cancel'),

    re_path(r'^echec-de-paiement',
        bank_fail, name='teleforma-bank-fail'),

    re_path(r'^accounts/(?P<username>[A-Za-z0-9+@._-]+)/receipt/download/$',
        ReceiptPDFViewDownload.as_view(), name="teleforma-receipt-download"),
    re_path(r'^accounts/(?P<username>[A-Za-z0-9+@._-]+)/receipt/view/$',
        ReceiptPDFView.as_view(), name="teleforma-receipt-view"),

    # chat
    path('chat/messages',
         ChatMessageView.as_view(), name='teleforma-chat-messages'),
    # notification
    path('notification',
         NotificationView.as_view(), name='teleforma-notification'),

    # must be called on channels instance
    path('live_conference_notify',
        LiveConferenceNotify.as_view(), name='teleforma-live-conference-notify'),

    # QUIZ
    re_path(r'^desk/periods/(?P<period_id>.*)/courses/(?P<course_id>.*)/quiz/(?P<quiz_name>[\w-]+)/$', QuizQuestionView.as_view(), name="teleforma-quiz"),
]
