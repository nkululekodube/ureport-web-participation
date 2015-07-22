from django.apps import apps

CELERY_IMPORTS = ("apps.send_token.tasks", )

BROKER_URL = "redis://localhost:6379"

CELERY_TIMEZONE = 'Africa/Nairobi'

CELERY_RESULT_BACKEND = "redis"
