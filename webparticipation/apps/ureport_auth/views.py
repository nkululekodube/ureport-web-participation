from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _

from webparticipation.apps.ureport_auth import tasks
from webparticipation.apps.ureport_auth.models import PasswordReset
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.ureporter.views import is_valid_password
from webparticipation.apps.latest_poll.decorators import show_untaken_latest_poll_message


@show_untaken_latest_poll_message
def login_user(request):
    backend = 'django.contrib.auth.backends.ModelBackend'

    if request.method == 'GET':
        redirect_to = request.GET.get('next', '/shout')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_to = request.POST.get('next', '/shout')
        user = User.objects.filter(email=email).first()
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
                messages.error(request, _('Password is incorrect'))
        else:
            messages.warning(request, _('There is no registered user with sign-in email %s' % email))

    return render_to_response('login.html', RequestContext(request, {'next': redirect_to}))


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            tasks.send_forgot_password_email.delay(email)
            return render(request, 'forgot_password.html', {
                'success_message': _('We have sent an email to %s with recovery instructions. Please check your email.')
                % email,
                'password_reset_email_sent': True})
        else:
            messages.error(request, _('There is no registered user with sign-in email %s') % str(email))
    return render_to_response('forgot_password.html', RequestContext(request))


def password_reset(request, reset_token):
    password_reset = PasswordReset.objects.filter(token=reset_token).first()

    if request.method == 'GET':
        if not password_reset or not password_reset.expiry > timezone.now():
            messages.error(request, _('Sorry that recovery link is expired. Please Try again.'))
            return HttpResponseRedirect('/forgot-password/')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user = User.objects.get(username=password_reset.user.username)

        if password == confirm_password:
            if is_valid_password(password):
                user.set_password(password)
                user.save()
                password_reset.delete()
                messages.info(request, _('Password successfully changed for %s') % user.email)
                return HttpResponseRedirect('/login/')
            else:
                messages.error(request, _('Password should have a minimum of 8 characters.'))
        else:
            messages.error(request, _('Password do not match.'))

    return render_to_response('password_reset.html', RequestContext(request))
