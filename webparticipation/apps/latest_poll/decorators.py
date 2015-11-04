from webparticipation.apps.latest_poll.models import LatestPoll
from webparticipation.apps.poll_response.views import complete_run_already_exists
from webparticipation.apps.ureporter.models import Ureporter


def show_untaken_latest_poll_message(view_func):
    def _decorated(request, *args, **kwargs):
        if request.GET.get('lp', True):
            latest_poll = LatestPoll.get_solo()
            if request.user and latest_poll.flow_uuid and request.user.is_authenticated():
                uuid = Ureporter.objects.get(user=request.user).uuid
                request.session.lp = not complete_run_already_exists(latest_poll.flow_uuid, uuid)
        return view_func(request, *args, **kwargs)

    return _decorated
