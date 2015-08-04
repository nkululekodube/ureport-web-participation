from django.shortcuts import render
from webparticipation.apps.ureporter.models import Ureporter


def home(request):
    uuid = None
    if Ureporter.objects.filter(user__username=request.user).exists():
        ureporter = Ureporter.objects.get(user__username=request.user)
        if ureporter:
            uuid = ureporter.uuid
    return render(request, 'index.html', {'uuid': uuid})
