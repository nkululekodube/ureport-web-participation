from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from random import randint
from time import sleep
import requests
import tasks
from webparticipation.apps.ureport_user.models import UreportUser
from webparticipation.apps.utils.views import dashify_user, undashify_user


messages = []


def register(request):
    user = get_user(request)
    response = HttpResponse()

    if request.method == 'GET':
        if user_is_authenticated(request):
            response = render(request, 'register.html', {'messages': [{'msg_text': "You're already registered!"}]})
        else:
            requests.post(settings.RAPIDPRO_RECEIVED_PATH, data={ 'from': undashify_user(user), 'text': 'webregister' })
            response = render(request, 'register.html', {'messages': get_messages_for_user(user)})
            response.set_cookie(key='uuid', value=user)

    if request.method == 'POST':
        requests.post(settings.RAPIDPRO_RECEIVED_PATH, data={ 'from': undashify_user(user), 'text': request.POST['send'] })
        messages = get_messages_for_user(user)
        response = render(request, 'register.html', {'messages': messages})

    return response


def user_is_authenticated(request):
    return request.COOKIES.get('uuid')


def get_user(request):
    if user_is_authenticated(request):
        return request.COOKIES.get('uuid')
    else:
        rand_seed = 'user' + str(randint(100000000, 999999999))
        contact = requests.post(settings.RAPIDPRO_API_PATH + '/contacts.json',
            data={'urns': ['tel:' + rand_seed]},
            headers={'Authorization': 'Token ' + settings.RAPIDPRO_API_TOKEN})
        uuid = contact.json()['uuid']
        UreportUser(uuid=uuid).save()
        return uuid


def get_messages_for_user(user_id):
    global messages
    while not len(messages):
        sleep(.5)
    return filter_messages(user_id)


def filter_messages(user_id):
    global messages
    filtered_messages = filter(lambda msg: msg['msg_to'] == undashify_user(user_id), messages)
    messages = filter(lambda msg: msg['msg_to'] != undashify_user(user_id), messages)
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
