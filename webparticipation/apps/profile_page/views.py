from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET

from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.latest_poll.decorators import show_untaken_latest_poll_message


@login_required
@show_untaken_latest_poll_message
def view_profile(request):
    ureporter = Ureporter.objects.get(user__username=request.user)
    confirm_changes = False
    if request.method == 'POST':
        ureporter.subscribed = True if request.POST.get('subscribed') == 'True' else False
        ureporter.save()
        confirm_changes = True
    return render(request, 'profile.html', {'uuid': ureporter.uuid,
                                            'email': ureporter.user.email,
                                            'date_joined': ureporter.user.date_joined,
                                            'subscribed': ureporter.subscribed,
                                            'confirm_changes': confirm_changes})


@login_required
@require_http_methods(['GET', 'POST'])
def deactivate_account(request):
    ureporter = Ureporter.objects.get(user__username=request.user)
    if request.method == 'GET':
        return render(
            request,
            'deactivate.html',
            {'uuid': ureporter.uuid, 'email': ureporter.user.email, 'is_active': ureporter.user.is_active})
    elif request.method == 'POST':
        ureporter.delete()
        return HttpResponseRedirect('/profile/goodbye')


@require_GET
def goodbye(request):
    return render(request, 'goodbye.html')


@require_http_methods(['GET', 'POST'])
@require_GET
def unsubscribe_account(request, unsubscribe_token):
    ureporter = Ureporter.objects.filter(unsubscribe_token=unsubscribe_token).first()
    if ureporter:
        ureporter.subscribed = False
        ureporter.save()
        return render(request, 'unsubscribe.html', {'user_exists': True})
    return render(request, 'unsubscribe.html', {'user_exists': False})
