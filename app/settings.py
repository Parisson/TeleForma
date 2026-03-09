# -*- coding: utf-8 -*-
# Django settings for sandbox project.

# Monkey-patches for django-json-rpc (abandoned, incompatible with Py3.13/Django5)
import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

from django.utils import encoding as _enc
if not hasattr(_enc, 'smart_text'):
    _enc.smart_text = _enc.smart_str
if not hasattr(_enc, 'force_text'):
    _enc.force_text = _enc.force_str

from django.utils import translation as _trans
if not hasattr(_trans, 'ugettext'):
    _trans.ugettext = _trans.gettext
if not hasattr(_trans, 'ugettext_lazy'):
    _trans.ugettext_lazy = _trans.gettext_lazy
if not hasattr(_trans, 'ugettext_noop'):
    _trans.ugettext_noop = _trans.gettext_noop
if not hasattr(_trans, 'ungettext'):
    _trans.ungettext = _trans.ngettext
if not hasattr(_trans, 'ungettext_lazy'):
    _trans.ungettext_lazy = _trans.ngettext_lazy

from django.utils.encoding import force_str
import warnings
import os
import sys
import socket
from django.urls import reverse_lazy


########################
# ADMIN / SECURITY
########################

ADMINS = (
    ('Guillaume Pellerin', 'webmaster@parisson.com'),
    ('Gael le Mignot', 'gael@pilotsystems.net'),
    #    ('Admin CRFPA', 'admin-crfpa@pre-barreau.com'),
)

MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a8l7%06wr2k+3=%#*#@#rvop2mmzko)44%7k(zx%lls^ihm9^5'

ALLOWED_HOSTS = ['localhost', 'crfpa.dockdev.pilotsystems.net',
    'staging.docker.e-learning.crfpa.pre-barreau.parisson.com',
    'e-learning.crfpa.pre-barreau.com',
    'prod.docker.e-learning.crfpa.pre-barreau.parisson.com',
    'recovery.docker.e-learning.crfpa.pre-barreau.parisson.com',
    'channels'
]


########################
# SYSTEM
########################

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.dont_write_bytecode = True

DEBUG_ENV = os.environ.get('DEBUG') == 'True'
DEBUG = DEBUG_ENV
DEBUG_TOOLBAR = False
RECOVERY = False

INTERNAL_IPS = ['127.0.0.1', ]

# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']

ASGI_APPLICATION = "teleforma.ws.routing.application"

warnings.showwarning = lambda *x: None
SILENCED_SYSTEM_CHECKS = ["fields.W342"]
if not DEBUG:
    SILENCED_SYSTEM_CHECKS += ["urls.W003", "urls.W005"]

ROOT_URLCONF = 'urls'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

########################
# DATABASES
########################

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql',
        # Or path to database file if using sqlite3.
        'NAME': os.environ.get('POSTGRES_DATABASE'),
        # Not used with sqlite3.
        'USER': os.environ.get('POSTGRES_USER'),
        # Not used with sqlite3.
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': os.environ.get('DB_HOST'),
        # Set to empty string for default. Not used with sqlite3.
        'PORT': os.environ.get('DB_PORT'),
    },
}

if RECOVERY:
    DATABASES['recovery'] = {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql',
        # Or path to database file if using sqlite3.
        'NAME': os.environ.get('POSTGRES_DATABASE'),
        # Not used with sqlite3.
        'USER': os.environ.get('POSTGRES_USER'),
        # Not used with sqlite3.
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD_RECOVERY'),
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': os.environ.get('DB_HOST_RECOVERY'),
        # Set to empty string for default. Not used with sqlite3.
        'PORT': os.environ.get('DB_PORT'),
        }


########################
# LANGUAGE / ZONE
########################

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

USE_TZ = False


########################
# MEDIA / STATIC
########################

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://pre-barreau.com/archives/'
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'

MEDIA_S3_BUCKET = '/media/bucket/'

FILE_UPLOAD_TEMP_DIR = '/tmp'

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


########################
# TEMPLATES
########################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'app', 'templates')],
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
                'teleforma.context_processors.debug',
            ],
        },
    },
]


########################
# CACHE
########################

# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
   'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memcached:11211',
        'TIMEOUT': None,
        'OPTIONS': {
            'no_delay': True,
            'ignore_exc': True,
            'max_pool_size': 16,
            'use_pooling': True,
        }
   }
}

CACHE_TIMEOUT = 60*60*24

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}


########################
# LOGGING
########################

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
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': "/var/log/app/app.log",
            'formatter': 'simple',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
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


########################
# APPS / MIDDLEWARE
########################

MIDDLEWARE = (('debug_toolbar.middleware.DebugToolbarMiddleware',) if DEBUG_TOOLBAR else ()) + (
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    'teleforma.middleware.XsSharing',
    'django_user_agents.middleware.UserAgentMiddleware',
    "django.middleware.common.CommonMiddleware",
)

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
    'django_recaptcha',
    'django_nvd3',
    'tinymce',
    'pdfannotator',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'quiz',
    'multichoice',
    'true_false',
    'essay',
    'corsheaders',
)


########################
# DEBUG
########################

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ('debug_toolbar',)

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }


########################
# REDIS
########################

REDIS_HOST = "redis"
REDIS_PORT = 6379


########################
# CHANNELS
########################

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# channel access point from django
if DEBUG:
    CHANNEL_URL = "http://channels:8000"
else:
    CHANNEL_URL = "/var/run/app/asgi.sock"


########################
# AUTH / SESSIONS
########################

AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = reverse_lazy('teleforma-desk')

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

def show_user_as(user):
    professor = user.professor.all()
    is_corrector = False
    if user.quotas.count() and not professor and not user.is_superuser:
        return "#"+str(user.id)
    else:
        return force_str(user)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
#SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
#SESSION_ENGINE = "unique_session.backends.session_backend"
UNIQUE_SESSION_WHITELIST = (1, 2042)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SAMESITE="None"
SESSION_COOKIE_SECURE=True


########################
# JAZZMIN
########################

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


########################
# TINYMCE
########################

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


########################
# SHERLOCK
########################

SHERLOKS_URL = "https://sherlocks-payment-webinit-simu.secure.lcl.fr/paymentInit"

PAYMENT_PARAMETERS = { 'Semestrielle': { 'merchantId' : "002001000000003",
                                         '_key': "002001000000003_KEY1",
                                         'keyVersion': '1',
                                         'currencyCode': '978',
                                        },
                       'Annuelle': { 'merchantId' : "002001000000003",
                                     '_key': "002001000000003_KEY1",
                                     'keyVersion': '1',
                                     'currencyCode': '978',
                                    },
                       'Estivale': { 'merchantId' : "002001000000003",
                                     '_key': "002001000000003_KEY1",
                                     'keyVersion': '1',
                                     'currencyCode': '978',
                                    },
                      }
SHERLOKS_USE_TRANSACTION_ID = True


########################
# WEBPACK
########################

USE_WEBPACK_DEV_SERVER = False
WEBPACK_DEV_SERVER_URL = "http://172.24.104.152:3000/"


########################
# POSTMAN
########################

POSTMAN_SHOW_USER_AS = show_user_as
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_DISALLOW_ANONYMOUS = True


########################
# TELEFORMA
########################

TELEFORMA_ORGANIZATION = 'Pré-Barreau - CRFPA'
TELEFORMA_SUBJECTS = ('Barreau', 'CRFPA', 'e-learning')
TELEFORMA_DESCRIPTION = "E-learning Pré-Barreau - CRFPA"
TELEFORMA_E_LEARNING_TYPE = 'CRFPA'
TELEFORMA_GLOBAL_TWEETER = False
TELEFORMA_PERIOD_TWEETER = True
TELEFORMA_EXAM_TOPIC_DEFAULT_DOC_TYPE_ID = 4
TELEFORMA_EXAM_SCRIPT_UPLOAD = True
TELEFORMA_ADMIN = "Admin-CRFPA"
TELEFORMA_REGISTER_DEFAULT_DOC_ID = 5506
TELEFORMA_PERIOD_DEFAULT_ID = 34
TELEFORMA_EXAM_MAX_SESSIONS = 200
TELEFORMA_EXAM_SCRIPT_MAX_SIZE = 31457280
TELEFORMA_EXAM_SCRIPT_SERVICE_URL = '/webviewer/teleforma.html'
TELEFORMA_EXAM_USE_S3 = True
TELEFORMA_PRIVATE_DOCUMENTS_MODE = True
TELEFORMA_PRIVATE_MEDIA_USE_S3 = True
TELEFORMA_MEDIA_DOWNLOAD = False

ORAL_OPTION_PRICE = 250
FASICLE_OPTION_PRICE = 110
# use to share correction doc / media accross different training
CORRECTIONS_COURSE_TYPE_ID = 2

ENABLE_CHAT = True
CHAT_LIMIT_HOURS = 48

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

#THUMBNAIL_FORCE_OVERWRITE = True


########################
# EMAIL
########################

EMAIL_HOST = 'angus.parisson.com'
DEFAULT_FROM_EMAIL = 'crfpa@pre-barreau.com'
SERVER_EMAIL = 'crfpa@pre-barreau.com'
EMAIL_SUBJECT_PREFIX = '[' + TELEFORMA_ORGANIZATION + '] '


########################
# TELECASTER
########################

TELECASTER_LIVE_STREAMING_PROTOCOL = 'https'
TELECASTER_LIVE_STREAMING_SERVER = 'jimmy.parisson.com'
TELECASTER_LIVE_STREAMING_SERVERS = ['jimmy.parisson.com', 'bbb3.parisson.com', 'malcom.parisson.com']
TELECASTER_LIVE_RANDOM_SERVERS = True
TELECASTER_LIVE_STREAMING_PORT = 443
TELECASTER_LIVE_ICECAST_STREAMING_PORT = 443
TELECASTER_LIVE_ICECAST_STREAMING_PATH = '/stream/audio/'
TELECASTER_LIVE_STREAM_M_STREAMING_PORT = 443
TELECASTER_LIVE_STREAM_M_STREAMING_PATH = '/stream/video/'
TELECASTER_LIVE_TWEETER = False


########################
# RECAPTCHA
########################

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_REQUIRED_SCORE = 0.85


########################
# AWS S3
########################

AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""
AWS_S3_REGION_NAME=""
AWS_S3_ENDPOINT_URL=""
AWS_S3_ENCRYPTION=True
AWS_S3_FILE_OVERWRITE=False

########################
# BBB
########################

BBB_LOGO_URL = "/static/teleforma/images/pb/logo_pb_2025.png"
BBB_PDF_URL = "/static/teleforma/pdf/pb-blank-slide.pdf"
BBB_BANNER_COLOR = "#003768"

########################
# CORS
########################

CORS_ALLOWED_ORIGINS = [
    "https://e-learning.pre-barreau.com",
]

CORS_ALLOW_ALL_ORIGINS = False

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

