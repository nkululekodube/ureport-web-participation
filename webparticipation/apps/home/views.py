from django.shortcuts import render

from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.latest_poll.decorators import show_untaken_latest_poll_message


@show_untaken_latest_poll_message
def home(request):
    uuid = None
    if Ureporter.objects.filter(user__username=request.user).exists():
        ureporter = Ureporter.objects.get(user__username=request.user)
        if ureporter:
            uuid = ureporter.uuid
    return render(request, 'index.html', {'uuid': uuid})
