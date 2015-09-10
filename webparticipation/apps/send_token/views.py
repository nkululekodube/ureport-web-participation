from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webparticipation.apps.ureporter.models import Ureporter
from . import tasks


@csrf_exempt
def send_token(request):
    if request.method == 'POST':
        urn_tel = request.POST.get('phone')
        email_address = request.POST.get('text')
        session_ureporter = Ureporter.objects.get(urn_tel=urn_tel)
        existing_ureporter = Ureporter.objects.filter(user__email=email_address).first()
        if existing_ureporter:
            tasks.delete_user_from_rapidpro(existing_ureporter)
            existing_ureporter.uuid = session_ureporter.uuid
            existing_ureporter.urn_tel = session_ureporter.urn_tel
            existing_ureporter.user.username = session_ureporter.user.username
            session_ureporter.delete()
            existing_ureporter.save()
            if not existing_ureporter.token:
                data = {'send_token': 'exists'}
            else:
                data = {'send_token': 'send'}
                tasks.send_verification_token.delay(existing_ureporter)
        else:
            session_ureporter.user.email = email_address
            session_ureporter.save()
            data = {'send_token': 'send'}
            tasks.send_verification_token.delay(session_ureporter)

        response = JsonResponse(data)
        response.status_codecode = 200
        return response
