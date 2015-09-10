from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureporter.models import Ureporter


@csrf_exempt
def confirm_token(request):
    if request.method == 'POST':
        request_params = request.POST.dict()
        token = int(request_params['text'])
        username = request_params['phone']
        user = Ureporter.objects.get(user__username=username)

        data = None
        if user.token == token:
            data = {'token_ok': 'true'}
        else:
            data = {'token_ok': 'false'}

        response = JsonResponse(data)
        response.status_code = 200
        return response
