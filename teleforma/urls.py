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
from django.conf.urls.defaults import *
from django.views.generic import *
from django.views.generic.base import *
from teleforma.models import *
from teleforma.views import *
from telemeta.views import *
from jsonrpc import jsonrpc_site

htdocs_forma = os.path.dirname(__file__) + '/static/teleforma/'
user_export = UsersXLSExport()
profile_view = ProfileView()
document = DocumentView()
media = MediaView()

urlpatterns = patterns('',
#    url(r'^$', HomeView.as_view(), name='teleforma-home'),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'telemeta/login.html'},
        name="teleforma-login"),

    # Telemeta
    url(r'^', include('telemeta.urls')),

    # Help
    url(r'^help/$', HelpView.as_view(), name="teleforma-help"),

    # Desk
    url(r'^desk/$', CoursesView.as_view(), name="teleforma-desk"),
    url(r'^desk/courses/(?P<pk>.*)/$', CourseView.as_view(), name="teleforma-course-detail"),

    url(r'^desk/medias/(?P<pk>.*)/detail/$', MediaView.as_view(), name="teleforma-media-detail"),
    url(r'^desk/medias/(?P<pk>.*)/download/$', media.download, name="teleforma-media-download"),

    url(r'^desk/documents/(?P<pk>.*)/detail/$', DocumentView.as_view(),
        name="teleforma-document-detail"),
    url(r'^desk/documents/(?P<pk>.*)/download/$', document.download,
        name="teleforma-document-download"),
    url(r'^desk/documents/(?P<pk>.*)/view/$', document.view,
        name="teleforma-document-view"),
#    url(r'^desk/documents/(?P<pk>.*)/view/$', document_view, name="teleforma-document-view"),

    url(r'^desk/conferences/(?P<pk>.*)/video/$',
        ConferenceView.as_view(),
        name="teleforma-conference-detail"),
    url(r'^desk/conferences/(?P<pk>.*)/audio/$',
        ConferenceView.as_view(template_name="teleforma/course_conference_audio.html"),
        name="teleforma-conference-audio"),
    url(r'^desk/conference_record/$', ConferenceRecordView.as_view(),
        name="teleforma-conference-record"),

    # Postman
    url(r'^messages/', include('postman.urls')),

    # Users
    url(r'^users/$', UsersView.as_view(), name="teleforma-users"),
    url(r'^users/(?P<username>[A-Za-z0-9._-]+)/profile/$', profile_view.profile_detail,
                               name="teleforma-profile-detail"),
    url(r'^users/(?P<id>.*)/login/$', UserLoginView.as_view(), name="teleforma-user-login"),
    url(r'^users/all/export/$', user_export.all, name="teleforma-users-xls-export"),

    url(r'^users/by_training/(\w+)/$', UsersTrainingView.as_view(), name="teleforma-training-users"),
    url(r'^users/by_training/(?P<id>.*)/export/$', user_export.by_training,
        name="teleforma-training-users-export"),

    url(r'^users/by_iej/(\w+)/$', UsersIejView.as_view(), name="teleforma-iej-users"),
    url(r'^users/by_iej/(?P<id>.*)/export/$', user_export.by_iej, name="teleforma-iej-users-export"),

    url(r'^users/by_course/(\w+)/$', UsersCourseView.as_view(), name="teleforma-course-users"),
    url(r'^users/by_course/(?P<id>.*)/export/$', user_export.by_course,
        name="teleforma-course-users-export"),


# CSS+Images (FIXME: for developement only)
    url(r'^teleforma/css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': htdocs_forma+'css'},
        name="teleforma-css"),
    url(r'images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': htdocs_forma+'images'},
        name="teleforma-images"),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': htdocs_forma+'js'},
        name="teleforma-js"),

    # JSON RPC
    url(r'json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),

#    url(r'^private_files/', include('private_files.urls')),

    # JQCHAT
    url(r'^', include('jqchat.urls')),

)
