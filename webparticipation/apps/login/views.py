from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext


def login_user(request):
    backend = 'django.contrib.auth.backends.ModelBackend'

    if request.method == 'GET':
        redirect_to = request.GET.get('next', '/')
        return render_to_response('login.html', RequestContext(request,  {'next': redirect_to}))

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_to = request.POST.get('next', '/')
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, 'Email not registered. Please try again.')

        if user:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                authenticated_user.backend = backend
                if user.is_active:
                    login(request, authenticated_user)
                    return HttpResponseRedirect(redirect_to)
            else:
                messages.warning(request, 'Password is incorrect')

        return render_to_response('login.html', RequestContext(request,  {'next': redirect_to}))
