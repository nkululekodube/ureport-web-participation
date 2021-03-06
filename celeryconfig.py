from datetime import timedelta

CELERY_IMPORTS = ('webparticipation.apps.send_token.tasks',
                  'webparticipation.apps.ureport_auth.tasks',
                  'webparticipation.apps.latest_poll.tasks',)

BROKER_URL = 'redis://localhost:6379'

CELERY_TIMEZONE = 'Africa/Nairobi'

CELERY_RESULT_BACKEND = 'redis'

CELERYBEAT_SCHEDULE = {
    'retrieve_latest_poll': {
        'task': 'latest_poll.retrieve_latest_poll',
        'schedule': timedelta(minutes=1),
        'relative': True,
    },
}
