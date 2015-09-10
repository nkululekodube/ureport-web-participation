from test import *

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