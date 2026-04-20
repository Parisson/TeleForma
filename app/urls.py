# -*- coding: utf-8 -*-
import os

from django.conf.urls import include
from django.urls import re_path
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http import HttpResponse
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()

js_info_dict = ['teleforma']

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

urlpatterns = [
    # Example:
    # (r'^sandbox/', include('sandbox.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),

    # TeleForma
    re_path(r'^', include('teleforma.urls')),

    # Languages
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=js_info_dict), name="js_catalog"),
    re_path(r'^robots\.txt$', lambda r: HttpResponse(
        "User-agent: *\nDisallow: /", mimetype="text/plain")),

    re_path(r'^tinymce/', include('tinymce.urls')),
    #re_path(r'^pdfviewer/', include('webviewer.urls')),
    re_path(r'^pdfannotator/', include('pdfannotator.urls')),
    re_path(r'^messages/', include('postman.urls', namespace='postman')),
] + ([re_path(r'^__debug__/', include(debug_toolbar.urls)),] if settings.DEBUG_TOOLBAR else [])

