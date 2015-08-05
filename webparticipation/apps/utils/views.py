import requests
import os
import re


def send_message_to_rapidpro(data):
    requests.post(os.environ.get('RAPIDPRO_RECEIVED_PATH'), data=data)


def undashify_user(user):
    return user.replace('-', '')


def dashify_user(user):
    return user[:8] + '-' + user[8:12] + '-' + user[12:16] + '-' + user[16:20] + '-' + user[20:]


def is_valid_password(password_string):
    matches_regex = re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password_string)
    return matches_regex
