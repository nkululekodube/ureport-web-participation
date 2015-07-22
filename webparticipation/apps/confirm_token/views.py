from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureport_user.models import UreportUser
from webparticipation.apps.utils.views import dashify_user
# from . import tasks


@csrf_exempt
def confirm_token(response):
    if response.method == 'POST':
        response_params = response.POST.dict()
        submitted_code = response_params['text']
        user_id = dashify_user(response_params['phone'])
        user = UreportUser.objects.get(uuid=user_id)

        resp = HttpResponse()
        if str(user.token) == submitted_code:
            user.active = True
            user.token = 0
            user.save()
            resp.status_code = 200
        else:
            resp.status_code = 403
        return resp
