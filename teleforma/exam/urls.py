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
from teleforma.exam.models import *
from teleforma.exam.views import *
from jsonrpc import jsonrpc_site


urlpatterns = patterns('',

    url(r'^desk/periods/(?P<period_id>.*)/exam/script/(?P<pk>.*)/detail/$', ScriptView.as_view(),
        name="teleforma-exam-script-detail"),

    url(r'^desk/periods/(?P<period_id>.*)/exam/scripts/list/$', ScriptsView.as_view(),
        name="teleforma-exam-script-list"),

    url(r'^desk/periods/(?P<period_id>.*)/exam/scripts_pending/$', ScriptsPendingView.as_view(), name="teleforma-exam-scripts-pending"),
    url(r'^desk/periods/(?P<period_id>.*)/exam/scripts_treated/$', ScriptsTreatedView.as_view(), name="teleforma-exam-scripts-treated"),
    url(r'^desk/periods/(?P<period_id>.*)/exam/scripts_rejected/$', ScriptsRejectedView.as_view(), name="teleforma-exam-scripts-rejected"),

)
