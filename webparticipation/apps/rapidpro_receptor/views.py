from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests


@csrf_exempt
def rapidpro_receptor(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        send_received_confirmation_to_rapidpro(request_params)
        broadcast_rapidpro_response(request_params)
        return HttpResponse('OK')


def send_received_confirmation_to_rapidpro(request_params):
    requests.post(os.environ.get.RAPIDPRO_RECEIVED_PATH, data={
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
