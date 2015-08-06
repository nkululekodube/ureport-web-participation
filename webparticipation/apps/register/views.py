from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from random import randint
import requests
import os
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import send_message_to_rapidpro, undashify_user
from webparticipation.apps.rapidpro_receptor.views import get_messages_for_user, rapidpro_dispatcher_callback

messages = settings.MESSAGES


def register(request):
    ureporter = get_user(request)
    uuid = ureporter.uuid
    if request.method == 'GET':
        return serve_get_response(request, uuid)
    if request.method == 'POST':
        return serve_post_response(request, uuid, ureporter)


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
    api_path = os.environ.get('RAPIDPRO_API_PATH')
    rapidpro_api_token = os.environ.get('RAPIDPRO_API_TOKEN')
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


def serve_get_response(request, uuid):
    undashified_uuid = undashify_user(uuid)
    if user_is_authenticated(request):
        return get_already_registered_message(request)
    else:
        send_message_to_rapidpro({'from': undashified_uuid, 'text': 'webregister'})
        return render(request, 'register.html', {'messages': get_messages_for_user(uuid),
                                                 'uuid': uuid})


def user_is_authenticated(request):
    return request.user.is_authenticated()


def get_already_registered_message(request):
    return render(request, 'register.html', {
        'messages': [{'msg_text': _("You're already logged in. Why don't you take our latest poll?")}]})


def serve_post_response(request, uuid, ureporter):
    undashified_uuid = undashify_user(uuid)
    if request.POST.get('password'):
        activate_user(request, ureporter)
        send_message_to_rapidpro({'from': undashified_uuid, 'text': 'next'})
    else:
        send_message_to_rapidpro({'from': undashified_uuid, 'text': request.POST['send']})
    messages = get_messages_for_user(uuid)
    return render(request, 'register.html', {
        'messages': messages,
        'last_submission': request.POST.get('send') or None,
        'is_password': has_password_keyword(messages),
        'uuid': uuid})


def activate_user(request, ureporter):
    ureporter.user.set_password(request.POST.get('password'))
    ureporter.invalidate_token()
    ureporter.user.is_active = True
    ureporter.save()


def has_password_keyword(messages):
    return bool([message for message in messages if message['msg_text'].find('password') != -1])


settings.RAPIDPRO_DISPATCHER.connect(rapidpro_dispatcher_callback)
