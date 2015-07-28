from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import dashify_user
from . import tasks


@csrf_exempt
def send_token(request):
    if request.method == 'POST':
        email_address = request.POST.get('text')
        email_exists = Ureporter.objects.filter(email=email_address).exists()
        if email_exists:
            session_user = Ureporter.objects.get(uuid=get_uuid(request))
            existing_user = Ureporter.objects.get(email=email_address)
            existing_user.set_uuid(session_user.uuid)
            session_user.delete()
            if not existing_user.token:
                data = {'send_token': 'exists'}
            else:
                data = {'send_token': 'send'}
                tasks.send_verification_token.delay(existing_user)
        else:
            user = Ureporter.objects.get(uuid=get_uuid(request))
            user.set_email(email_address)
            data = {'send_token': 'send'}
            tasks.send_verification_token.delay(user)

        response = JsonResponse(data)
        response.status_code = 200
        return response


def get_uuid(request):
    return dashify_user(request.POST.get('phone'))
