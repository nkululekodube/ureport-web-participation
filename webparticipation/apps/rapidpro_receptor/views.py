import datetime
import re
from time import sleep

import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext as _
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
    start_time = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=10)
    while not MessageBus.objects.filter(msg_to=username).exists():
        time_now = datetime.datetime.now()
        if time_now > start_time + timeout:
            return [_('Sorry, something went wrong.')], False
        else:
            sleep(.5)
    sleep(2) # two seconds for all message for that ureporter to come in
    sorted_message_ids = get_sorted_message_ids(username)
    messages_from_rapidpro = get_messages_from_rapidpro_api(sorted_message_ids)
    full_text_messages = [msg['results'][0]['text'] for msg in messages_from_rapidpro]
    return full_text_messages, True


def get_sorted_message_ids(username):
    filtered_messages = get_filtered_messages(username)
    sorted_message_ids = sorted(list(set([msg.msg_id for msg in filtered_messages])))
    remove_messages_from_message_bus(username)
    return sorted_message_ids


def get_filtered_messages(username):
    filtered_messages = MessageBus.objects.filter(msg_to=username)
    len(filtered_messages)
    return filtered_messages


def remove_messages_from_message_bus(username):
    MessageBus.objects.filter(msg_to=username).delete()


def get_messages_from_rapidpro_api(sorted_message_ids):
    messages = [get_message_from_rapidpro_api_by_id(id) for id in sorted_message_ids]
    return messages


def get_message_from_rapidpro_api_by_id(id):
    return requests.get(settings.RAPIDPRO_API_PATH + '/messages.json?id=' + str(id),
                        headers={'Authorization': 'Token ' + settings.RAPIDPRO_API_TOKEN}).json()


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
    return bool([msg for msg in msgs if re.search(_('^.+[P|p]assword.+$'), msg)])


settings.RAPIDPRO_DISPATCHER.connect(append_rapidpro_message_to_message_bus)
