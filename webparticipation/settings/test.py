"""Development settings and globals."""

from common import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS += (
    'django_pdb',
)

MIDDLEWARE_CLASSES += (
    'django_pdb.middleware.PdbMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CELERY_ALWAYS_EAGER = True

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += (
    'behave_django',
    'django_coverage'
)

COVERAGE_MODULE_EXCLUDES = ('solo', 'kombu', 'djcelery', 'django','bootstrap3', 'compressor')
