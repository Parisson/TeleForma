# -*- coding: utf-8 -*-
# Django settings for sandbox project.

import os
import sys
from django.core.urlresolvers import reverse_lazy
import environ

sys.dont_write_bytecode = True

env = environ.Env(DEBUG=(bool, False),
                  CELERY_ALWAYS_EAGER=(bool, False),
                  )

# Django settings for server project.
DEBUG = env('DEBUG')  # False if not in os.environ
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Guillaume Pellerin', 'webmaster@parisson.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'USER': env('MYSQL_USER'),      # Not used with sqlite3.
        'PASSWORD': env('MYSQL_PASSWORD'),  # Not used with sqlite3.
        'NAME': env('MYSQL_DATABASE'),
        'HOST': 'db',      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',   # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'fr_FR'
LANGUAGES = [ ('fr', 'French'),
              ('en', 'English'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')

if not os.path.exists(MEDIA_ROOT):
	os.mkdir(MEDIA_ROOT)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8040/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a8l7%06wr2k+3=%#*#@#rvop2mmzko)44%7k(zx%lls^ihm9^5'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader', (
#        'django.template.loaders.filesystem.Loader',
#        'django.template.loaders.app_directories.Loader',
#    )),
#)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/momo/dev/teleforma/teleforma/teleforma/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'telemeta',
    'jsonrpc',
    # 'south',
    'teleforma',
    'sorl.thumbnail',
    'django_extensions',
    'pagination',
    'postman',
    # 'private_files',
    # 'markup_mixin',
    #'notes',
    # 'jquery',
    'timezones',
    'jqchat',
    # 'follow',
    # 'googletools',
    'telecaster',
    'multichoice',
    'true_false',
    'essay',
    'quiz',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'postman.context_processors.inbox',
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "teleforma.context_processors.periods",
)

BROKER_URL = env('BROKER_URL')
CELERY_IMPORTS = ("timeside.server.tasks",)
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']

from worker import app

HAYSTACK_CONNECTIONS = {
    'default': {
        #'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'ENGINE': 'telemeta.util.backend.CustomElasticEngine',
        'URL': env('HAYSTACK_URL'),
        'INDEX_NAME': env('HAYSTACK_INDEX_NAME'),
        'INLUDE_SPELLING': True,
        'EXCLUDED_INDEXES': ['telemeta.search_indexes.LocationIndex',
                             'telemeta.search_indexes.LocationAliasIndex',
                             'telemeta.search_indexes.InstrumentIndex',
                             'telemeta.search_indexes.InstrumentAliasIndex'
                             ]
    },
    'autocomplete': {
        # 'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'ENGINE': 'telemeta.util.backend.CustomElasticEngine',
        'URL': env('HAYSTACK_URL'),
        'INDEX_NAME': env('HAYSTACK_INDEX_NAME_AUTOCOMPLETE'),
        'INLUDE_SPELLING': True,
        'EXCLUDED_INDEXES': ['telemeta.search_indexes.MediaItemIndex',
                             'telemeta.search_indexes.MediaCollectionIndex',
                             'telemeta.search_indexes.MediaCorpusIndex',
                             'telemeta.search_indexes.MediaFondsIndex'
                             ]
    },
}

HAYSTACK_ROUTERS = ['telemeta.util.search_router.AutoRouter', 'haystack.routers.DefaultRouter']
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SIGNAL_PROCESSOR = 'telemeta.util.search_signals.RealTimeCustomSignal'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

BOWER_COMPONENTS_ROOT = '/srv/bower/'
BOWER_PATH = '/usr/local/bin/bower'
BOWER_INSTALLED_APPS = (
    'jquery#2.2.4',
    'jquery-migrate#~1.2.1',
    'underscore#1.8.3',
    'bootstrap#3.3.7',
    'bootstrap-select#1.5.4',
    'font-awesome#4.4.0',
    'angular#1.2.26',
    'angular-bootstrap-select#0.0.5',
    'angular-resource#1.2.26',
    'raphael#2.2.7',
    'soundmanager#V2.97a.20150601',
    'jquery-ui#1.11.4',
    'tablesorter',
    'video.js',
    'sass-bootstrap-glyphicons',
    # 'https://github.com/Parisson/loaders.git',
    # 'https://github.com/Parisson/ui.git',
)

NOTEBOOK_DIR = MEDIA_ROOT + 'notebooks'
if not os.path.exists(NOTEBOOK_DIR):
    os.makedirs(NOTEBOOK_DIR)

NOTEBOOK_ARGUMENTS = [
    '--ip=0.0.0.0', # reach notebooks from outside
    '--port=8888',  # std port
    '--no-browser', # don't start browser on start
    '--allow-root',
    '--notebook-dir', NOTEBOOK_DIR
]

SILENCED_SYSTEM_CHECKS = ['fields.W342',]


TELEMETA_ORGANIZATION = 'Pre-Barreau - CRFPA'
TELEMETA_SUBJECTS = ('test', 'telemeta', 'sandbox')
TELEMETA_DESCRIPTION = "Telemeta TEST sandbox"
TELEMETA_GMAP_KEY = 'ABQIAAAArg7eSfnfTkBRma8glnGrlxRVbMrhnNNvToCbZQtWdaMbZTA_3RRGObu5PDoiBImgalVnnLU2yN4RMA'
TELEMETA_CACHE_DIR = MEDIA_ROOT + 'cache'
TELEMETA_EXPORT_CACHE_DIR = TELEMETA_CACHE_DIR + "/export"
TELEMETA_DATA_CACHE_DIR = TELEMETA_CACHE_DIR + "/data"

TELEMETA_DOWNLOAD_ENABLED = True
TELEMETA_STREAMING_FORMATS = ('mp3', 'webm')
TELEMETA_DOWNLOAD_FORMATS = ('wav', 'mp3', 'webm')
TELEMETA_PUBLIC_ACCESS_PERIOD = 51
TELEMETA_DEFAULT_GRAPHER_SIZES = ['360x130', '640x130']
TELEMETA_DEFAULT_GRAPHER_ID = 'waveform_contour_wh'

AUTH_PROFILE_MODULE = 'telemeta.userprofile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = reverse_lazy('teleforma-desk')
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

EMAIL_HOST = 'smtp.numericable.fr'
DEFAULT_FROM_EMAIL = 'webmaster@parisson.com'
SERVER_EMAIL = 'webmaster@parisson.com'
EMAIL_SUBJECT_PREFIX = '[' + TELEMETA_ORGANIZATION.decode('utf8') + '] '

POSTMAN_AUTO_MODERATE_AS = True

TELEFORMA_E_LEARNING_TYPE = 'CRFPA'
TELEFORMA_GLOBAL_TWEETER = False
TELEFORMA_PERIOD_TWEETER = True
TELEFORMA_EXAM_TOPIC_DEFAULT_DOC_TYPE_ID = 4
TELEFORMA_EXAM_SCRIPT_UPLOAD = True
TELEFORMA_REGISTER_DEFAULT_DOC_ID = 5506
TELEFORMA_PERIOD_DEFAULT_ID = 12
TELEFORMA_EXAM_MAX_SESSIONS = 15
TELEFORMA_EXAM_SCRIPT_MAX_SIZE = 20480000
TELEFORMA_EXAM_SCRIPT_SERVICE_URL = '/webviewer/teleforma.html'

TELECASTER_LIVE_STREAMING_SERVER = 'stream.parisson.com'
TELECASTER_LIVE_STREAMING_PORT = 443

TELECASTER_CONF = [{'type':'mp3','server_type':'icecast','conf':'/etc/telecaster/deefuzzer_mp3.xml', 'port':'8000'},
                   {'type':'webm','server_type':'stream-m','conf':'/etc/telecaster/deefuzzer_webm.xml', 'port':'8080'}, ]

TELECASTER_RSYNC_SERVER = 'telecaster@jimi.parisson.com:archives/'
TELECASTER_RSYNC_LOG = '/var/log/telecaster/rsync.log'
TELECASTER_MASTER_SERVER = 'angus.parisson.com'

TELECASTER_LIVE_STREAMING_SERVER = 'stream.parisson.com'
TELECASTER_LIVE_STREAMING_PORT = 443
TELECASTER_LIVE_ICECAST_STREAMING_PORT = 8000
TELECASTER_LIVE_STREAM_M_STREAMING_PORT = 8888

# CRFPA or AE or PRO
TELEFORMA_E_LEARNING_TYPE = 'CRFPA'
TELEFORMA_GLOBAL_TWEETER = False
TELEFORMA_PERIOD_TWEETER = True

JQCHAT_DISPLAY_COUNT = 50
JQCHAT_DISPLAY_TIME  = 48
