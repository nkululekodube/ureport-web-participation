from django.http import HttpResponseRedirect
from django.conf import settings

from webparticipation.apps.latest_poll.decorators import show_untaken_latest_poll_message


@show_untaken_latest_poll_message
def home(request):
    return HttpResponseRedirect(settings.UREPORT_ROOT)
