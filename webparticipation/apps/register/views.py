import re
import os
import requests
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _
from webparticipation.apps.ureporter.views import get_user, activate_user
from webparticipation.apps.utils.views import undashify_user
from webparticipation.apps.rapidpro_receptor.views import get_messages_for_user, rapidpro_dispatcher_callback

messages = settings.MESSAGES


def register(request):
    ureporter = get_user(request)
    uuid = ureporter.uuid
    if request.method == 'GET':
        return serve_get_response(request, uuid)
    if request.method == 'POST':
        return serve_post_response(request, uuid, ureporter)


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


def has_password_keyword(messages):
    return bool([message for message in messages if re.match('.+[P|p]assword.+', message['msg_text'])])


def send_message_to_rapidpro(data):
    response = requests.post(os.environ.get('RAPIDPRO_RECEIVED_PATH'), data=data)
    return response


settings.RAPIDPRO_DISPATCHER.connect(rapidpro_dispatcher_callback)
