from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from random import randint
from time import sleep
import requests
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import send_message_to_rapidpro, undashify_user
import os
from django.contrib.auth.models import User

messages = []


def register(request):
    ureporter = get_user(request)
    uuid = ureporter.uuid
    undashified_uuid = undashify_user(uuid)
    response = HttpResponse()

    if request.method == 'GET':
        if user_is_authenticated(request):
            response = get_already_registered_message(request)
        else:
            send_message_to_rapidpro({'from': undashified_uuid, 'text': 'webregister'})
            response = render(request, 'register.html', {'messages': get_messages_for_user(uuid)})
            response.set_cookie(key='uuid', value=uuid)

    if request.method == 'POST':
        if request.POST.get('password'):
            ureporter.user.set_password(request.POST.get('password'))
            ureporter.invalidate_token()
            ureporter.user.is_active = True
            ureporter.user.save()
            send_message_to_rapidpro({'from': undashified_uuid, 'text': 'next'})
        else:
            send_message_to_rapidpro({'from': undashified_uuid, 'text': request.POST['send']})

        messages = get_messages_for_user(uuid)
        response = render(request, 'register.html', {
            'messages': messages,
            'last_submission': request.POST.get('send') or None,
            'is_password': has_password_keyword(messages)})

    return response


def get_user(request):
    if user_is_authenticated(request):
        uuid = request.COOKIES.get('uuid')
        return Ureporter.objects.get(uuid=uuid)
    else:
        contact = requests.post(os.environ.get('RAPIDPRO_API_PATH') + '/contacts.json',
                                data={'urns': ['tel:' + generate_random_seed()]},
                                headers={'Authorization': 'Token ' + os.environ.get('RAPIDPRO_API_TOKEN')})
        uuid = contact.json()['uuid']
        ureporter = Ureporter(uuid=uuid, user=User.objects.create_user(generate_random_seed()))
        ureporter.user.is_active = False
        ureporter.user.save()
        ureporter.save()
        return ureporter


def user_is_authenticated(request):
    return request.COOKIES.get('uuid')


def get_already_registered_message(request):
    return render(request, 'register.html', {'messages': [
        {'msg_text': "You're already logged in. Why don't you take our latest poll?"}]})


def generate_random_seed():
    return 'user' + str(randint(100000000, 999999999))


def has_password_keyword(messages):
    return [message for message in messages if message['msg_text'].find('password') != -1]


def get_messages_for_user(uuid):
    global messages
    while not len(messages):
        sleep(.5)
    return filter_messages(uuid)


def filter_messages(uuid):
    global messages
    filtered_messages = filter(lambda msg: msg['msg_to'] == undashify_user(uuid), messages)
    messages = filter(lambda msg: msg['msg_to'] != undashify_user(uuid), messages)
    return filtered_messages


def rapidpro_dispatcher_callback(sender, **kwargs):
    global messages
    messages.append({
        'msg_id': kwargs['param_id'],
        'msg_channel': kwargs['param_channel'],
        'msg_from': kwargs['param_from'],
        'msg_to': kwargs['param_to'],
        'msg_text': kwargs['param_text']
    })


settings.RAPIDPRO_DISPATCHER.connect(rapidpro_dispatcher_callback)
