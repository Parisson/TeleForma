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
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from teleforma.models import *
from teleforma.views import *
from telemeta.views import *
from teleforma.forms import *
from registration.views import *
from jsonrpc import jsonrpc_site

htdocs_forma = os.path.dirname(__file__) + '/static/teleforma/'
profile_view = ProfileView()
document = DocumentView()
media = MediaView()

urlpatterns = patterns('',


    # login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'telemeta/login.html'},
        name="teleforma-login"),
    # (r'^accounts/register0/$', RegistrationView.as_view(), {'form_class':CustomRegistrationForm}),
    url(r'^accounts/register/$', UserAddView.as_view(), name="teleforma-register"),
    url(r'^accounts/complete/$', UserCompleteView.as_view(), name="teleforma-register-complete"),
    url(r'^captcha/', include('captcha.urls')),

    # Help
    url(r'^help/$', HelpView.as_view(), name="teleforma-help"),

    # Home
    url(r'^$', HomeRedirectView.as_view(), name="teleforma-home"),

    # Telemeta
    url(r'^', include('telemeta.urls')),

    # Desk
    url(r'^desk/$', HomeRedirectView.as_view(), name="teleforma-desk"),
    url(r'^desk/periods/(?P<period_id>.*)/courses/$', CourseListView.as_view(), name="teleforma-desk-period-list"),
    url(r'^desk/periods/(?P<period_id>.*)/courses/(?P<pk>.*)/detail/$', CourseView.as_view(),
        name="teleforma-desk-period-course"),

    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/detail/$', MediaView.as_view(), name="teleforma-media-detail"),
    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/embed/$', MediaViewEmbed.as_view(), name="teleforma-media-embed"),
    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/download/$', media.download, name="teleforma-media-download"),

    url(r'^desk/documents/(?P<pk>.*)/detail/$', DocumentView.as_view(),
        name="teleforma-document-detail"),
    url(r'^desk/documents/(?P<pk>.*)/download/$', document.download,
        name="teleforma-document-download"),
    url(r'^desk/documents/(?P<pk>.*)/view/$', document.view,
        name="teleforma-document-view"),

    url(r'^archives/annals/$', AnnalsView.as_view(), name="teleforma-annals"),
    url(r'^archives/annals/by-iej/(\w+)/$', AnnalsIEJView.as_view(), name="teleforma-annals-iej"),
    url(r'^archives/annals/by-course/(\w+)/$', AnnalsCourseView.as_view(), name="teleforma-annals-course"),

    url(r'^desk/periods/(?P<period_id>.*)/conferences/(?P<pk>.*)/video/$',
        ConferenceView.as_view(), name="teleforma-conference-detail"),
    url(r'^desk/periods/(?P<period_id>.*)/conferences/(?P<pk>.*)/audio/$',
        ConferenceView.as_view(template_name="teleforma/course_conference_audio.html"),
        name="teleforma-conference-audio"),
    url(r'^desk/conference_record/$', ConferenceRecordView.as_view(),
        name="teleforma-conference-record"),
    url(r'^desk/periods/(?P<period_id>.*)/conferences/list/$', ConferenceListView.as_view(),
        name="teleforma-conferences"),

    # Postman
    url(r'^messages/', include('postman.urls')),

    # Users
    url(r'^users/training/(?P<training_id>.*)/iej/(?P<iej_id>.*)/course/(?P<course_id>.*)/list/$',
        UsersView.as_view(), name="teleforma-users"),

    url(r'^users/training/(?P<training_id>.*)/iej/(?P<iej_id>.*)/course/(?P<course_id>.*)/export/$',
        UsersExportView.as_view(), name="teleforma-users-export"),

    url(r'^users/(?P<username>[A-Za-z0-9+@._-]+)/profile/$', profile_view.profile_detail,
                               name="teleforma-profile-detail"),

    url(r'^users/(?P<id>.*)/login/$', UserLoginView.as_view(), name="teleforma-user-login"),

    # JSON RPC
    url(r'json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),

#    url(r'^private_files/', include('private_files.urls')),

    # JQCHAT
    url(r'^', include('jqchat.urls')),

    # EXAM
    url(r'^', include('teleforma.exam.urls')),


)
