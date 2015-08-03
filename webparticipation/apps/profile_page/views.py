from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from webparticipation.apps.ureporter.models import Ureporter


@login_required
def view_profile(request, ureporter_uuid):
    user = Ureporter.objects.get(user__username=request.user)
    if user.uuid == ureporter_uuid:
        return render(request, 'profile.html', {'ureporter_uuid': ureporter_uuid})
    else:
        return render(request, '404.html', status=404)
