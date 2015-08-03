from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.utils.views import dashify_user
from . import tasks


@csrf_exempt
def send_token(request):
    if request.method == 'POST':
        email_address = request.POST.get('text')
        email_exists = Ureporter.objects.filter(user__email=email_address).exists()
        if email_exists:
            session_ureporter = Ureporter.objects.get(uuid=get_uuid(request))
            existing_ureporter = Ureporter.objects.get(user__email=email_address)
            existing_ureporter.set_uuid(session_ureporter.uuid)
            session_ureporter.delete()

            if not existing_ureporter.token:
                data = {'send_token': 'exists'}
            else:
                data = {'send_token': 'send'}
                tasks.send_verification_token.delay(existing_ureporter)
        else:
            ureporter = Ureporter.objects.get(uuid=get_uuid(request))
            ureporter.user.email = email_address
            ureporter.user.save()
            data = {'send_token': 'send'}
            tasks.send_verification_token.delay(ureporter)

        response = JsonResponse(data)
        response.status_codecode = 200
        return response


def get_uuid(request):
    return dashify_user(request.POST.get('phone'))
