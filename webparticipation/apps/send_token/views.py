from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureport_user.models import UreportUser
from webparticipation.apps.utils.views import dashify_user, undashify_user
from . import tasks


@csrf_exempt
def send_token(response):
    if response.method == 'POST':
        response_params = response.POST.dict()
        email_address = response_params['text']
        user = UreportUser.objects.get(uuid=dashify_user(response_params['phone']))
        user.email = email_address
        user.save()
        tasks.send_verification_token.delay(user)
        resp = HttpResponse()
        resp.status_code = 200
        return resp
