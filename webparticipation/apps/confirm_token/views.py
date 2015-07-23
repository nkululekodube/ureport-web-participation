from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureport_user.models import UreportUser
from webparticipation.apps.utils.views import dashify_user


@csrf_exempt
def confirm_token(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        submitted_code = request_params['text']
        uuid = dashify_user(request_params['phone'])
        user = UreportUser.objects.get(uuid=uuid)

        data = None
        if str(user.token) == submitted_code:
            data = {'token_ok': 'true'}
        else:
            data = {'token_ok': 'false'}

        response = JsonResponse(data)
        response.status_code = 200
        return response
