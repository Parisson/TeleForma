# -*- coding: utf-8 -*-
# Django settings for sandbox project.

import os
import sys
from django.core.urlresolvers import reverse_lazy

sys.dont_write_bytecode = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Guillaume Pellerin', 'webmaster@parisson.com'),
    ('Lists', 'lists@parisson.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'teleforma_exam.sql',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
MEDIA_URL = '/media/'

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
    'south',
    'teleforma',
    'teleforma.exam',
    'sorl.thumbnail',
    'django_extensions',
    'pagination',
    'postman',
#    'private_files',
    'markup_mixin',
    'notes',
#    'jquery',
    'timezones',
    'jqchat',
#    'follow',
     'googletools',
     # 'telecaster',
     'extra_views',
     'captcha',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'postman.context_processors.inbox',
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "teleforma.context_processors.periods",
    "teleforma.exam.context_processors.exam_access",
)

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

TELECASTER_CONF = [{'type':'mp3','server_type':'icecast','conf':'/etc/telecaster/deefuzzer_mp3.xml', 'port':'8000'},
                   {'type':'webm','server_type':'stream-m','conf':'/etc/telecaster/deefuzzer_webm.xml', 'port':'8080'}, ]

TELECASTER_RSYNC_SERVER = 'telecaster@jimi.parisson.com:archives/'
TELECASTER_RSYNC_LOG = '/var/log/telecaster/rsync.log'
TELECASTER_MASTER_SERVER = 'angus.parisson.com'

# CRFPA or AE or PRO
TELEFORMA_E_LEARNING_TYPE = 'CRFPA'
TELEFORMA_GLOBAL_TWEETER = False
TELEFORMA_PERIOD_TWEETER = True
TELEFORMA_EXAM_TOPIC_DEFAULT_DOC_TYPE_NUMBER = 2
TELEFORMA_EXAM_SCRIPT_UPLOAD = True

JQCHAT_DISPLAY_COUNT = 50
JQCHAT_DISPLAY_TIME  = 48

BOX_API_TOKEN = 'D2pBaN8YqjGIfS0tKrgnMP93'

SOUTH_MIGRATION_MODULES = {
    'captcha': 'captcha.south_migrations',
}
