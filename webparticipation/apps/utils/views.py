from django.conf import settings
import requests


def send_message_to_rapidpro(data):
    requests.post(settings.RAPIDPRO_RECEIVED_PATH, data=data)


def undashify_user(user):
    return user.replace('-', '')


def dashify_user(user):
    return user[:8] + '-' + user[8:12] + '-' + user[12:16] + '-' + user[16:20] + '-' + user[20:]
