from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureport_user.models import UreportUser
from webparticipation.apps.utils.views import dashify_user
from . import tasks


@csrf_exempt
def send_token(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        email_address = request_params['text']

        user_exists = None
        try:
            user_exists = UreportUser.objects.get(email=email_address)
        except UreportUser.DoesNotExist:
            pass

        if user_exists:
            data = {'send_token': 'exists'}
        else:
            data = {'send_token': 'send'}
            uuid = dashify_user(request_params['phone'])
            user = UreportUser.objects.get(uuid=uuid)
            user.email = email_address
            user.save()
            tasks.send_verification_token.delay(user)

        response = JsonResponse(data)
        response.status_code = 200
        return response
