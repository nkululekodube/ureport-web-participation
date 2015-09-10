from common import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CELERY_ALWAYS_EAGER = True

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webparticipation',
        'USER': os.environ.get('SNAP_DB_PG_USER'),
        'PASSWORD': os.environ.get('SNAP_DB_PG_PASSWORD'),
        'HOST': os.environ.get('SNAP_DB_PG_HOST'),
        'PORT': os.environ.get('SNAP_DB_PG_PORT'),
    }
}