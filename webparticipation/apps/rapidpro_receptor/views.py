import os
import re
import requests
from time import sleep
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from collections import OrderedDict

message_bus = settings.MESSAGE_BUS


@csrf_exempt
def rapidpro_receptor(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        broadcast_rapidpro_response(request_params)
        return HttpResponse('OK')


def send_message_to_rapidpro(data):
    response = requests.post(os.environ.get('RAPIDPRO_RECEIVED_PATH'), data=data)
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
    global message_bus
    while not len(message_bus):
        sleep(.5)
    return filter_messages(username)


def filter_messages(username):
    global message_bus
    filtered_messages = dedupe_messages([message for message in message_bus if message['msg_to'] == username])
    message_bus = [message for message in message_bus if message['msg_to'] != username]
    return filtered_messages


def dedupe_messages(msgs):
    return OrderedDict((frozenset(msg.items()), msg) for msg in msgs).values()


def append_rapidpro_message_to_message_bus(sender, **kwargs):
    global message_bus
    message_bus.append({
        'msg_id': kwargs['param_id'],
        'msg_channel': kwargs['param_channel'],
        'msg_from': kwargs['param_from'],
        'msg_to': kwargs['param_to'],
        'msg_text': kwargs['param_text']
    })


def has_password_keyword(msgs, username):
    return bool([msg for msg in msgs if re.match('.+[P|p]assword.+', msg['msg_text']) and msg['msg_to'] == username])


settings.RAPIDPRO_DISPATCHER.connect(append_rapidpro_message_to_message_bus)
