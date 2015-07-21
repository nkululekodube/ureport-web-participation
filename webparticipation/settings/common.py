"""Commonly shared settings and globals."""

from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath
from sys import path
import dispatch
import auth

RAPIDPRO_PROTOCOL = 'http://'
RAPIDPRO_HOST = 'localhost'
RAPIDPRO_PORT = '8000'
RAPIDPRO_PATH = '/api/v1/external/received/7a795bef-8c13-476e-9350-8799da09d362/' # Enter your own channel id here
RAPIDPRO_URL = RAPIDPRO_PROTOCOL + RAPIDPRO_HOST + ':' + RAPIDPRO_PORT + RAPIDPRO_PATH

RAPIDPRO_DISPATCHER = dispatch.Signal()

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

SITE_ROOT = dirname(DJANGO_ROOT)

SITE_NAME = basename(DJANGO_ROOT)

path.append(DJANGO_ROOT)

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'admin@admin.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
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

SECRET_KEY = r"fnm@j%xid5kxd8+^wgwz$b5vl_5vx9bjv+#4byn90%5%rq%h8^"

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
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
)

LOCAL_APPS = (
    'webparticipation.apps.register',
    'webparticipation.apps.rapidpro_receptor',
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

DEFAULT_FROM_EMAIL = auth.EMAIL_HOST_USER

SERVER_EMAIL = auth.SERVER_EMAIL

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = auth.EMAIL_HOST_USER

EMAIL_HOST_PASSWORD = auth.EMAIL_HOST_PASSWORD
