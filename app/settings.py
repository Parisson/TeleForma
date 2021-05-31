# -*- coding: utf-8 -*-
# Django settings for sandbox project.

from django.utils.encoding import force_text
import warnings
import os
import sys
from django.urls import reverse_lazy
# import environ

sys.dont_write_bytecode = True

DEBUG = True if os.environ.get('DEBUG') == 'True' else False
TEMPLATE_DEBUG = DEBUG


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

warnings.showwarning = lambda *x: None

ADMINS = (
    ('Guillaume Pellerin', 'webmaster@parisson.com'),
    ('Gael le Mignot', 'gael@pilotsystems.net'),
    #    ('Admin CRFPA', 'admin-crfpa@pre-barreau.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': os.environ.get('POSTGRES_DATABASE'),
        # Not used with sqlite3.
        'USER': os.environ.get('POSTGRES_USER'),
        # Not used with sqlite3.
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': 'postgres',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
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
LANGUAGE_CODE = 'fr'
LANGUAGES = [
    ('fr', 'French'),
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
MEDIA_ROOT = '/srv/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://pre-barreau.com/archives/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/srv/static/'

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
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # TODO : check if useless
    # 'pagination.middleware.PaginationMiddleware',
    'teleforma.middleware.XsSharing',
    'django_user_agents.middleware.UserAgentMiddleware',
)

ROOT_URLCONF = 'urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'south',
    'teleforma',
    'teleforma.webclass',
    'teleforma.exam',
    'jsonrpc',
    'sorl.thumbnail',
    # 'django_extensions',
    # 'pagination',
    'postman',
    # 'timezones',
    # 'googletools',
    # 'extra_views',
    'captcha',
    'django_nvd3',
    # 'bootstrap3',
    # 'bootstrap_pagination',
    # 'django_user_agents',
    'tinymce',
    # 'multichoice',
    # 'true_false',
    # 'essay',
    # 'quiz',
    'pdfannotator',
    # 'telemeta',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'postman.context_processors.inbox',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'teleforma.context_processors.periods',

            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TELEMETA_ORGANIZATION = 'Pré-Barreau - CRFPA'
TELEMETA_SUBJECTS = ('Barreau', 'CRFPA', 'e-learning')
TELEMETA_DESCRIPTION = "E-learning Pré-Barreau - CRFPA"
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

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'crfpa@pre-barreau.com'
SERVER_EMAIL = 'crfpa@pre-barreau.com'
EMAIL_SUBJECT_PREFIX = '[' + TELEMETA_ORGANIZATION + '] '

POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_DISALLOW_ANONYMOUS = True

#FILE_PROTECTION_METHOD = 'xsendfile'

TELEFORMA_ORGANIZATION = 'Pré-Barreau - CRFPA'
TELEFORMA_SUBJECTS = ('Barreau', 'CRFPA', 'e-learning')
TELEFORMA_DESCRIPTION = "E-learning Pré-Barreau - CRFPA"
TELEFORMA_E_LEARNING_TYPE = 'CRFPA'
TELEFORMA_GLOBAL_TWEETER = False
TELEFORMA_PERIOD_TWEETER = True
TELEFORMA_EXAM_TOPIC_DEFAULT_DOC_TYPE_ID = 4
TELEFORMA_EXAM_SCRIPT_UPLOAD = True
TELEFORMA_REGISTER_DEFAULT_DOC_ID = 5506
TELEFORMA_PERIOD_DEFAULT_ID = 22
TELEFORMA_EXAM_MAX_SESSIONS = 15
TELEFORMA_EXAM_SCRIPT_MAX_SIZE = 20480000
TELEFORMA_EXAM_SCRIPT_SERVICE_URL = '/webviewer/teleforma.html'

TELECASTER_LIVE_STREAMING_SERVER = 'stream4.parisson.com'
TELECASTER_LIVE_STREAMING_PORT = 443
TELECASTER_LIVE_ICECAST_STREAMING_PORT = 8000
TELECASTER_LIVE_STREAM_M_STREAMING_PORT = 8080

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

BOX_API_TOKEN = 'D2pBaN8YqjGIfS0tKrgnMP93'

FILE_UPLOAD_TEMP_DIR = '/tmp'

#SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_ENGINE = "unique_session.backends.session_backend"
UNIQUE_SESSION_WHITELIST = (1, 2042)

# SOUTH_MIGRATION_MODULES = {
#     'captcha': 'captcha.south_migrations',
# }

# Cache backend is optional, but recommended to speed up user agent parsing
# CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
# }

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

AUTH_USER_MODEL = 'auth.User'

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

# Sherlock's online payment
PAYMENT_SHERLOCKS_PATH = '/opt/sherlocks2'
PAYMENT_PARAMETERS = {'merchant_id': {'Semestrielle': "040109417200053",
                                      'Estivale': "040109417200054", },
                      'merchant_country': 'fr',
                      'currency_code': '978',
                      'language': 'fr'
                      }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': "/var/log/app.log",
            'formatter': 'simple',
        },
    },
    'loggers': {
        'payment': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


def show_user_as(user):
    professor = user.professor.all()
    is_corrector = False
    if user.quotas.count() and not professor and not user.is_superuser:
        return "#"+str(user.id)
    else:
        return force_text(user)


POSTMAN_SHOW_USER_AS = show_user_as

#THUMBNAIL_FORCE_OVERWRITE = True

ALLOWED_HOSTS = [ 'crfpa.dockdev.pilotsystems.net' ]
