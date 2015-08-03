from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from webparticipation.apps.login.tasks import send_forgot_password_email
from webparticipation.apps.ureporter.models import Ureporter


def login_user(request):
    backend = 'django.contrib.auth.backends.ModelBackend'

    if request.method == 'GET':
        redirect_to_url(request, 'login.html', '/')

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

        return render_to_response('login.html', RequestContext(request, {'next': redirect_to}))


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                send_forgot_password_email.delay(email)
            messages.info(request, 'Email recovery link sent to ' + email)

        except User.DoesNotExist:
            messages.warning(request, 'Email does not match any registered user.')

    return render_to_response('forgot_password.html', RequestContext(request))


def password_reset(request):
    redirect_to = request.POST.get('next', '/')

    if request.method == 'POST':
        redirect_to = request.POST.get('next', '/')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        uuid = request.POST.get('uuid')

        if password == confirm_password:
            user = User.objects.get(uuid=uuid)
            updated_user = Ureporter.objects.get(user=user).set_password(password)
            updated_user.save()
        else:
            messages.error(request, 'Password do not match.')
    return render_to_response('password_reset.html', RequestContext(request, {'next': redirect_to}))


def redirect_to_url(request, template, url):
    redirect_to = request.GET.get('next', url)
    return render_to_response(template, RequestContext(request, {'next': redirect_to}))
