# -*- coding: utf-8 -*-
import os

from django.conf.urls import include, url
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
    url(r'^admin/', admin.site.urls),

    # TeleForma
    url(r'^', include('teleforma.urls')),

    # Languages
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=js_info_dict), name="js_catalog"),
    url(r'^robots\.txt$', lambda r: HttpResponse(
        "User-agent: *\nDisallow: /", mimetype="text/plain")),

    url(r'^tinymce/', include('tinymce.urls')),
    #url(r'^pdfviewer/', include('webviewer.urls')),
    url(r'^pdfannotator/', include('pdfannotator.urls')),
    url(r'^messages/', include('postman.urls', namespace='postman')),
] + ([url(r'^__debug__/', include(debug_toolbar.urls)),] if settings.DEBUG_TOOLBAR else [])

