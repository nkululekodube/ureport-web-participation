import re
from time import sleep

import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from webparticipation.apps.message_bus.models import MessageBus


@csrf_exempt
def rapidpro_receptor(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        broadcast_rapidpro_response(request_params)
        return HttpResponse('OK')


def send_message_to_rapidpro(data):
    response = requests.post(settings.RAPIDPRO_RECEIVED_PATH, data=data)
    return response


def broadcast_rapidpro_response(request_params):
    settings.RAPIDPRO_DISPATCHER.send(
        sender=request_params['from'],
        param_id=request_params['id'],
        param_channel=request_params['channel'],
        param_from=request_params['from'],
        param_to=request_params['to'],
        param_text=request_params['text'])


def get_messages_for_user(username):
    while not MessageBus.objects.filter(msg_to=username).exists():
        sleep(.5)
    return filter_messages(username)


def filter_messages(username):
    filtered_messages = MessageBus.objects.filter(msg_to=username)
    len(filtered_messages)
    MessageBus.objects.filter(msg_to=username).delete()
    return filtered_messages


def append_rapidpro_message_to_message_bus(sender, **kwargs):
    if not is_duplicate_message(kwargs):
        MessageBus.objects.create(
            msg_id=kwargs['param_id'],
            msg_channel=kwargs['param_channel'],
            msg_to=kwargs['param_to'],
            msg_from=kwargs['param_from'],
            msg_text=kwargs['param_text'])


def is_duplicate_message(kwargs):
    return MessageBus.objects.filter(
        msg_id=kwargs['param_id'],
        msg_channel=kwargs['param_channel'],
        msg_to=kwargs['param_to'],
        msg_from=kwargs['param_from'],
        msg_text=kwargs['param_text']
    ).exists()


def has_password_keyword(msgs, username):
    return bool([msg for msg in msgs if re.search('^.+[P|p]assword.+$', msg.msg_text)])


settings.RAPIDPRO_DISPATCHER.connect(append_rapidpro_message_to_message_bus)
