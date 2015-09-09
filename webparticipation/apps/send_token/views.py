from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureporter.models import Ureporter
from . import tasks


@csrf_exempt
def send_token(request):
    if request.method == 'POST':
        email_address = request.POST.get('text')
        email_exists = Ureporter.objects.filter(user__email=email_address).exists()
        urn_tel = request.POST.get('phone')
        if email_exists:
            session_ureporter = Ureporter.objects.get(urn_tel=urn_tel)
            existing_ureporter = Ureporter.objects.get(user__email=email_address)
            tasks.delete_user_from_rapidpro(existing_ureporter)
            existing_ureporter.set_uuid(session_ureporter.uuid)
            session_ureporter.delete()
            if not existing_ureporter.token:
                data = {'send_token': 'exists'}
            else:
                data = {'send_token': 'send'}
                tasks.send_verification_token.delay(existing_ureporter)
        else:
            ureporter = Ureporter.objects.get(urn_tel=urn_tel)
            ureporter.user.email = email_address
            ureporter.save()
            data = {'send_token': 'send'}
            tasks.send_verification_token.delay(ureporter)

        response = JsonResponse(data)
        response.status_codecode = 200
        return response
