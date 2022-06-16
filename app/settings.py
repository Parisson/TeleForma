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
TESTING = False # mezzanine 
TEMPLATE_DEBUG = DEBUG

RECOVERY = True

DEBUG_TOOLBAR = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

warnings.showwarning = lambda *x: None

ADMINS = (
    ('Guillaume Pellerin', 'webmaster@parisson.com'),
    ('Gael le Mignot', 'gael@pilotsystems.net'),
    #    ('Admin CRFPA', 'admin-crfpa@pre-barreau.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    'localhost', 
    'el.pro-barreau.dockdev.pilotsystems.net',
    'e-learning.pro-barreau.com',    
    'staging.el.pro-barreau.parisson.com'
]

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
        'HOST': os.environ.get('DB_HOST'),
        # Set to empty string for default. Not used with sqlite3.
        'PORT': os.environ.get('DB_PORT'),
    },
}

if RECOVERY:
    DATABASES['recovery'] = {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
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
SECRET_KEY = "46a9a380-8a68-490f-86ce-e10730211dfb5a37d4a6-0b20-4ef4-85c4-c0ecac63af79cab06d89-3705-4271-8b20-9bca99b84c29"

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
    'django_user_agents.middleware.UserAgentMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware'
)
print(MIDDLEWARE)

ROOT_URLCONF = 'urls'


INSTALLED_APPS = (
    'jazzmin',
    # 'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django_comments',
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
#    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    # "mezzanine.twitter",
    'teleforma',
    'django.contrib.admin',
    'jsonrpc',
    'sorl.thumbnail',
    'django_extensions',
    'postman',
    'dj_pagination',
    # 'markup_mixin',
    'notes',
    # 'timezones',
    # 'googletools',
    # 'jqchat',
    'tinymce',
    'pbcart',
    'forms_builder.forms',
    'quiz',
    'multichoice',
    'true_false',
    'essay',

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
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
                "teleforma.context_processors.all_seminars",
                "teleforma.context_processors.total_progress",
                'postman.context_processors.inbox', 
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

TELEFORMA_ORGANIZATION = 'Pro-Barreau'
TELEFORMA_SUBJECTS = ('Barreau', 'e-learning')
TELEFORMA_DESCRIPTION = "E-learning Pro-Barreau"
TELEFORMA_E_LEARNING_TYPE = 'AE'

EMAIL_HOST = 'pb-smtp.pilotsystems.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'e-learning@pro-barreau.com'
SERVER_EMAIL = 'webmaster@parisson.com'
REPORT_TO_EMAIL = ('kostya.rilov@pre-barreau.com', 'alexia.dcruz@pro-barreau.com')
ADMIN_USERNAME = 'Pro-Barreau'
EMAIL_SUBJECT_PREFIX = '[' + TELEFORMA_ORGANIZATION + '] '

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

FILE_UPLOAD_TEMP_DIR = '/tmp'

SESSION_ENGINE = "django.contrib.sessions.backends.db"
#SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
#SESSION_ENGINE = "unique_session.backends.session_backend"
UNIQUE_SESSION_WHITELIST = (1, 2042)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_DOMAIN=".pro-barreau.com"
SESSION_COOKIE_SAMESITE="None"
SESSION_COOKIE_SECURE=True

# RECAPTCHA_PUBLIC_KEY = '6Ldq5DgbAAAAADkKg19JXlhx6F1XUQDsrXfXqSP6'
# RECAPTCHA_PRIVATE_KEY = '6Ldq5DgbAAAAAOVDOeF2kH8i2e2VSNHpqlinbpAJ'
# RECAPTCHA_REQUIRED_SCORE = 0.85

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

CACHE_TIMEOUT = None

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

# MEZZANINE
GRAPPELLI_INSTALLED = False
COMMENTS_NUM_LATEST = 5

JAZZMIN_SETTINGS = {
    "site_title": "Probarreau - E-learning",
    "site_header": "Probarreau",
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
    "order_with_respect_to": ["auth", "teleforma", "teleforma.webclass"],

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
    "related_modal_active": False,

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

PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"

if DEBUG_TOOLBAR:
    def show_toolbar(request):
        return True
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }
DEBUG_TOOLBAR_PATCH_SETTINGS = False


FORMS_LABEL_MAX_LENGTH = 1024
FORMS_FIELD_MAX_LENGTH = 255
FORMS_BUILDER_USE_SITES = False


BBB_SERVER = "https://bbb2.parisson.com/bigbluebutton/"
# BBB_SECRET = "uOzkrTnWly1jusr0PYcrlwhvKhZG1ZYDOrSvxgP70" # bbb1
BBB_SECRET = "3q3t6GCsv4wZmQlaT1pPX5ijysxeXOn8Vtn9svZEyU" # bbb2
BBB_USE_WEBHOOKS = False

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

