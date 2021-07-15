# -*- coding: utf-8 -*-
# Django settings for sandbox project.

from django.utils.encoding import force_text
import warnings
import os
import sys
from django.urls import reverse_lazy
# import environ

sys.dont_write_bytecode = True

DEBUG_ENV = os.environ.get('DEBUG') == 'True'
DEBUG = DEBUG_ENV
TEMPLATE_DEBUG = DEBUG

# disable to debug websocket and improve performance
DEBUG_TOOLBAR = False


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

warnings.showwarning = lambda *x: None

ADMINS = (
    ('Guillaume Pellerin', 'webmaster@parisson.com'),
    ('Gael le Mignot', 'gael@pilotsystems.net'),
    #    ('Admin CRFPA', 'admin-crfpa@pre-barreau.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['localhost', 'crfpa.dockdev.pilotsystems.net',
    'staging.docker.e-learning.crfpa.pre-barreau.parisson.com',
    'e-learning.crfpa.pre-barreau.com',
]

ASGI_APPLICATION = "teleforma.ws.routing.application"

REDIS_HOST = "redis"
REDIS_PORT = 6379

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

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

MIDDLEWARE = (('debug_toolbar.middleware.DebugToolbarMiddleware',) if DEBUG_TOOLBAR else ()) + (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
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
    'teleforma',
    'jazzmin',
    'django.contrib.admin',
    'channels',
    'teleforma.webclass',
    'teleforma.exam',
    'jsonrpc',
    'sorl.thumbnail',
    'dj_pagination',
    'postman',
    'captcha',
    'django_nvd3',
    'tinymce',
    'pdfannotator',
    'rest_framework',
    'rest_framework.authtoken',
)


if DEBUG_TOOLBAR:
    INSTALLED_APPS += ('debug_toolbar',)

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

AUTH_PROFILE_MODULE = 'telemeta.userprofile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = reverse_lazy('teleforma-desk')

#if DEBUG:
#    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
TELEFORMA_PERIOD_DEFAULT_ID = 21
TELEFORMA_EXAM_MAX_SESSIONS = 99
TELEFORMA_EXAM_SCRIPT_MAX_SIZE = 20480000
TELEFORMA_EXAM_SCRIPT_SERVICE_URL = '/webviewer/teleforma.html'

EMAIL_HOST = 'angus.parisson.com'
DEFAULT_FROM_EMAIL = 'crfpa@pre-barreau.com'
SERVER_EMAIL = 'crfpa@pre-barreau.com'
EMAIL_SUBJECT_PREFIX = '[' + TELEFORMA_ORGANIZATION + '] '

TELECASTER_LIVE_STREAMING_PROTOCOL = 'https'
TELECASTER_LIVE_STREAMING_SERVER = 'stream7.parisson.com'
TELECASTER_LIVE_STREAMING_PORT = 443
TELECASTER_LIVE_ICECAST_STREAMING_PORT = 443
TELECASTER_LIVE_ICECAST_STREAMING_PATH = '/stream/audio/'
TELECASTER_LIVE_STREAM_M_STREAMING_PORT = 443
TELECASTER_LIVE_STREAM_M_STREAMING_PATH = '/stream/video/'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

BOX_API_TOKEN = 'D2pBaN8YqjGIfS0tKrgnMP93'

FILE_UPLOAD_TEMP_DIR = '/tmp'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
#SESSION_ENGINE = "unique_session.backends.session_backend"
UNIQUE_SESSION_WHITELIST = (1, 2042)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

RECAPTCHA_PUBLIC_KEY = '6Ldq5DgbAAAAADkKg19JXlhx6F1XUQDsrXfXqSP6'
RECAPTCHA_PRIVATE_KEY = '6Ldq5DgbAAAAAOVDOeF2kH8i2e2VSNHpqlinbpAJ'
RECAPTCHA_REQUIRED_SCORE = 0.85

# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
   'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memcached:11211',
        'TIMEOUT': 604800,
        'OPTIONS': {
            'MAX_ENTRIES': 36000,
        }
   }
}

CACHE_TIMEOUT = 120

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
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
            'filename': "/var/log/app/app.log",
            'formatter': 'simple',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'payment': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'websocket': {
            'handlers': ['console'],
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

JAZZMIN_SETTINGS = {
    "site_title": "CRFPA",
    "site_header": "CRFPA",
    "site_logo": "teleforma/images/logo_pb.png",

    # # Links to put along the top menu
    # "topmenu_links": [

    #     # Url that gets reversed (Permissions can be added)
    #     {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

    #     # external url that opens in a new window (Permissions can be added)
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

    #     # model admin to link to (Permissions checked against model)
    #     {"model": "auth.User"},

    #     # App with dropdown menu to all its models pages (Permissions checked against models)
    #     {"app": "books"},
    # ],

    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "teleforma", "teleforma.webclass", "teleforma.exam", "pdfannotator"],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "teleforma": [{
    #         "name": "Make Messages", 
    #         "url": "make_messages", 
    #         "icon": "fas fa-comments",
    #         "permissions": ["books.view_book"]
    #     }]
    # },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "teleforma.newsitem": "fas fa-newspaper",
        "teleforma.conference": "fas fa-users",
        "teleforma.document": "fas fa-file",
        "teleforma.student": "fas fa-user-graduate",
        "teleforma.professor": "fas fa-user-tie",
        "webclass.webclass": "fas fa-phone",
    },
    "related_modal_active": True,

    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}
# Sherlock's online payment
PAYMENT_SHERLOCKS_PATH='/srv/sherlocks'

PAYMENT_PARAMETERS = { 'merchant_id' : { 'Semestrielle': "014295303911111",
                                         'Estivale': "014295303911111",
                                         'Pré-estivale': "014295303911111", },
                       'merchant_country': 'fr',
                       'currency_code': '978',
                       'language': 'fr'
}


if DEBUG_TOOLBAR:
    def show_toolbar(request):
        return True
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }


USE_WEBPACK_DEV_SERVER = False
WEBPACK_DEV_SERVER_URL = "http://172.24.104.152:3000/"


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e

