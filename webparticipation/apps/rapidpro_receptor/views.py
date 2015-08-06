from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from time import sleep
import requests
import os
from webparticipation.apps.utils.views import undashify_user

messages = settings.MESSAGES


@csrf_exempt
def rapidpro_receptor(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        send_received_confirmation_to_rapidpro(request_params)
        broadcast_rapidpro_response(request_params)
        return HttpResponse('OK')


def send_received_confirmation_to_rapidpro(request_params):
    requests.post(os.environ.get('RAPIDPRO_RECEIVED_PATH'), data={
        'from': request_params['from'],
        'text': request_params['text']
    })


def broadcast_rapidpro_response(request_params):
    settings.RAPIDPRO_DISPATCHER.send(
        sender=request_params['to'],
        param_id=request_params['id'],
        param_channel=request_params['channel'],
        param_from=request_params['from'],
        param_to=request_params['to'],
        param_text=request_params['text'])


def get_messages_for_user(uuid):
    global messages
    while not len(messages):
        sleep(10)
    return filter_messages(uuid)


def filter_messages(uuid):
    global messages
    undashified_uuid = undashify_user(uuid)
    filtered_messages = filter(lambda msg: msg['msg_to'] == undashified_uuid, messages)
    messages = filter(lambda msg: msg['msg_to'] != undashified_uuid, messages)
    print uuid, messages
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
