from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def register(request):
    context = {}
    if request.method == 'GET':
        context = {'messages': request.GET.lists()}

    if request.method == 'POST':
        context = {'messages': request.POST['send']}

    return render(request, 'register.html', context)

