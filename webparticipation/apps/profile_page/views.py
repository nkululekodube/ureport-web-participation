from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from webparticipation.apps.ureporter.models import Ureporter


@login_required
def view_profile(request, ureporter_uuid):
    ureporter = Ureporter.objects.get(user__username=request.user)
    if ureporter.uuid == ureporter_uuid:
        return render(request, 'profile.html', {'uuid': ureporter_uuid,
                                                'email': ureporter.user.email,
                                                'date_joined': ureporter.user.date_joined})
    else:
        return render(request, '404.html', status=404)


def deactivate_account(request, ureporter_uuid):

    if request.method == 'GET':
        ureporter = Ureporter.objects.get(user__username=request.user)
        if ureporter.uuid == ureporter_uuid:
            return render(request, 'deactivate.html', {'uuid': ureporter_uuid,
                                                       'email': ureporter.user.email,
                                                       'is_active': ureporter.user.is_active})
        else:
            return render(request, '404.html', status=404)

    if request.method == 'POST':
        Ureporter.objects.get(user__username=request.user).delete()
        return render(request, 'deactivate.html', {'deleted': True})