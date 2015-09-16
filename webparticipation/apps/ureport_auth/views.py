from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.utils import timezone

from webparticipation.apps.ureport_auth import tasks
from webparticipation.apps.ureport_auth.models import PasswordReset
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.ureporter.views import is_valid_password
from webparticipation.apps.latest_poll.decorators import show_untaken_latest_poll_message


@show_untaken_latest_poll_message
def login_user(request):
    backend = 'django.contrib.auth.backends.ModelBackend'

    if request.method == 'GET':
        redirect_to = request.GET.get('next', '/index')
        # redirect_to = request.GET.get('next', '/home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_to = request.POST.get('next', '/index')
        # redirect_to = request.POST.get('next', '/home')
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, 'There is no registered user with sign-in email ' + email)
        if user:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                authenticated_user.backend = backend
                if user.is_active:
                    login(request, authenticated_user)
                    has_taken_latest_poll = Ureporter.objects.get(user__username=request.user).is_latest_poll_taken()
                    if has_taken_latest_poll:
                        return HttpResponseRedirect(redirect_to)
                    else:
                        return HttpResponseRedirect(redirect_to + '?lp=true')
            else:
                messages.error(request, 'Password is incorrect')

    return render_to_response('login.html', RequestContext(request, {'next': redirect_to}))


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                tasks.send_forgot_password_email.delay(email)
                return render(request, 'forgot_password.html', {
                    'success_message': 'We have sent an email to ' + email + ' with recovery instructions. ' +
                                       'Please check your email.',
                    'password_reset_email_sent': True})
        except User.DoesNotExist:
            messages.error(request, 'There is no registered user with sign-in email ' + str(email))
    return render_to_response('forgot_password.html', RequestContext(request))


def password_reset(request, reset_token):
    password_reset = PasswordReset.objects.filter(token=reset_token).first()

    if request.method == 'GET':
        if not password_reset or not password_reset.expiry > timezone.now():
            messages.error(request, 'Sorry that recovery link is expired. Please Try again.')
            return HttpResponseRedirect('/forgot-password/')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user = User.objects.get(username=password_reset.user.username)

        if password == confirm_password:
            if is_valid_password(password):
                user.set_password(password)
                user.save()
                messages.info(request, 'Password successfully changed for ' + user.email)
                return HttpResponseRedirect('/login/')
            else:
                messages.error(request, 'Password should have a minimum of '
                                        '8 characters.')
        else:
            messages.error(request, 'Password do not match.')
    return render_to_response('password_reset.html', RequestContext(request))
