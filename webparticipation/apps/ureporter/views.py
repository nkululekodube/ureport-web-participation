import re
from random import randint

import requests
from django.contrib.auth.models import User
from django.conf import settings

from models import Ureporter


def get_user(request):
    uuid = request.POST.get('uuid')
    if uuid:
        return Ureporter.objects.get(uuid=uuid)
    else:
        return create_new_ureporter()


def create_new_ureporter():
    contact = create_new_rapidpro_contact().json()
    uuid = contact['uuid']
    urn_tel = contact['urns'][0][4::]
    ureporter = save_new_ureporter(uuid, urn_tel)
    return ureporter


def create_new_rapidpro_contact():
    api_path = settings.RAPIDPRO_API_PATH
    rapidpro_api_token = settings.RAPIDPRO_API_TOKEN
    while True:
        urn_tel = generate_random_urn_tel()
        if not Ureporter.objects.filter(urn_tel=urn_tel).exists():
            return requests.post(api_path + '/contacts.json',
                                 data={'urns': ['tel:' + urn_tel]},
                                 headers={'Authorization': 'Token ' + rapidpro_api_token})


def save_new_ureporter(uuid, urn_tel):
    ureporter = Ureporter(uuid=uuid, urn_tel=urn_tel, user=User.objects.create_user(urn_tel))
    ureporter.user.is_active = False
    ureporter.save()
    return ureporter


def generate_random_urn_tel():
    return 'user' + str(randint(100000000, 999999999))


def activate_user(request, ureporter):
    ureporter.user.set_password(request.POST.get('password'))
    ureporter.invalidate_token()
    ureporter.user.is_active = True
    ureporter.save()
    return ureporter.user


def is_valid_password(password_string):
    matches_regex = re.match(r'[A-Za-z0-9-@#$%^&+=]{8,}', password_string)
    if matches_regex:
        return True
    else:
        return False
