from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import requests

def rapidpro_receptor(request):
    print request.method
    if request.method == 'POST':
        post_data = {
            'from': request.POST['to'],
            'text': request.POST['text']
        }
        requests.post('http://localhost:8000/api/v1/external/received/7a795bef-8c13-476e-9350-8799da09d362/',
            data=post_data)
        return HttpResponse('OK')
