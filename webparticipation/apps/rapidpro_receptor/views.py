from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests, dispatch

@csrf_exempt
def rapidpro_receptor(response):
    if response.method == 'POST':
        response_params = response.POST.dict()
        send_received_confirmation_to_rapidpro(response_params)
        broadcast_rapidpro_response(response_params)
        return HttpResponse('OK')

def send_received_confirmation_to_rapidpro(response_params):
    requests.post(settings.RAPIDPRO_URL, data={ 'from': response_params['from'], 'text': response_params['text'] })

def broadcast_rapidpro_response(response_params):
    broadcast = settings.RAPIDPRO_DISPATCHER.send(
        sender=response_params['to'],
        param_id=response_params['id'],
        param_channel=response_params['channel'],
        param_from=response_params['from'],
        param_to=response_params['to'],
        param_text=response_params['text'])
    print 'broadcast', broadcast
