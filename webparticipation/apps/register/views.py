from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from random import randint
from time import sleep
import requests

messages = []

def register(request):
    response = HttpResponse()
    context = {}
    user = get_user(request)

    if request.method == 'GET':
        requests.post(settings.RAPIDPRO_URL, data={ 'from': user, 'text': 'webregister' })
        while not len(messages):
            sleep(.5)
        filtered_messages = filter_messages(user)
        response = render(request, 'register.html', {'messages': filtered_messages})
        response.set_cookie(key='userid', value=user)

    if request.method == 'POST':
        requests.post(settings.RAPIDPRO_URL, data={ 'from': user, 'text': request.POST['send'] })
        response = render(request, 'register.html', {'messages': messages})

    print request.method + ' messages', messages
    return response

def get_user(request):
    return request.COOKIES.get('userid') or 'user' + str(randint(100000000, 999999999))

def filter_messages(user_id):
    global messages
    filtered_messages = filter(lambda msg: msg['msg_to'] == user_id, messages)
    messages = filter(lambda msg: msg['msg_to'] != user_id, messages) # remove messages for this user
    return filtered_messages

def rapidpro_dispatcher_callback(sender, **kwargs):
    print 'dispatcher', sender, kwargs['param_id'], kwargs['param_channel'], kwargs['param_from'], kwargs['param_to'], kwargs['param_text']
    global messages
    messages.append({
        'msg_id': kwargs['param_id'],
        'msg_channel': kwargs['param_channel'],
        'msg_from': kwargs['param_from'],
        'msg_to': kwargs['param_to'],
        'msg_text': kwargs['param_text']
    })
    print 'messages', messages

settings.RAPIDPRO_DISPATCHER.connect(rapidpro_dispatcher_callback)
