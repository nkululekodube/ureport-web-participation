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

        status_code = 403
        data = {}
        if str(user.token) == submitted_code:
            user.active = True
            user.token = 0
            user.save()
            status_code = 200
            data = {'status': 200}
        else:
            data = {'status': 403}
        response = JsonResponse(data)
        response.status_code = status_code
        return response
