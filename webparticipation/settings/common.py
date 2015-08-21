"""Commonly shared settings and globals."""

from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath
from sys import path
import dispatch
import os

MESSAGE_BUS = []

RAPIDPRO_DISPATCHER = dispatch.Signal()

APPEND_SLASH = True

ALLOWED_HOSTS = os.environ.setdefault("ALLOWED_HOSTS", "127.0.0.1")

APP_HOST = ""

SERVER_NAME = ""

SECRET_KEY = os.environ.get('SECRET_KEY')

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

LOGIN_URL = '/login/'

SITE_ROOT = dirname(DJANGO_ROOT)

SITE_NAME = basename(DJANGO_ROOT)

PASSWORD_RESET_EXPIRY_DAYS = 1

TOKEN_EXPIRY_DAYS = 1

path.append(DJANGO_ROOT)

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'admin@admin.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webparticipation',
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

TIME_ZONE = 'Africa/Nairobi'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

MEDIA_URL = '/media/'

STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

FIXTURE_DIRS = (
    normpath(join(DJANGO_ROOT, 'fixtures')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = '%s.urls' % SITE_NAME

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'compressor',
    'djcelery',
    'solo',
)

LOCAL_APPS = (
    'webparticipation.apps.ureporter',
    'webparticipation.apps.register',
    'webparticipation.apps.rapidpro_receptor',
    'webparticipation.apps.send_token',
    'webparticipation.apps.confirm_token',
    'webparticipation.apps.utils',
    'webparticipation.apps.home',
    'webparticipation.apps.profile_page',
    'webparticipation.apps.ureport_auth',
    'webparticipation.apps.latest_poll',
    'webparticipation.apps.message_bus',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

CELERY_CHORD_PROPAGATES = True

WSGI_APPLICATION = 'wsgi.application'

COMPRESS_ENABLED = True

COMPRESS_CSS_HASHING_METHOD = 'content'

COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
