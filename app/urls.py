# -*- coding: utf-8 -*-
import os

from django.conf.urls import include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()

js_info_dict = ['teleforma']

DEBUG_ENV = os.environ.get('DEBUG') == 'True'

if DEBUG_ENV:
    import debug_toolbar

urlpatterns = [
    # Example:
    # (r'^sandbox/', include('sandbox.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url("^mezzanine/", include("mezzanine.urls")),

    # TeleForma
    url(r'^', include('teleforma.urls')),

    # Languages
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=js_info_dict), name="js_catalog"),
] + ([url(r'^__debug__/', include(debug_toolbar.urls)),] if DEBUG_ENV else [])

