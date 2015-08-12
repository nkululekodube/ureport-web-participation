from django.shortcuts import render
from django.utils.translation import ugettext as _
from webparticipation.apps.ureporter.views import get_user, activate_user
from webparticipation.apps.rapidpro_receptor.views import send_message_to_rapidpro, has_password_keyword, \
    get_messages_for_user
from webparticipation.apps.ureporter.models import Ureporter


def register(request):
    ureporter = get_user(request)
    uuid = ureporter.uuid
    if request.method == 'GET':
        return serve_get_response(request, uuid)
    if request.method == 'POST':
        return serve_post_response(request, uuid, ureporter)


def serve_get_response(request, uuid):
    username = Ureporter.objects.get(uuid=uuid).urn_tel
    if user_is_authenticated(request):
        return get_already_registered_message(request)
    else:
        send_message_to_rapidpro({'from': username, 'text': 'webregister'})
        return render(request, 'register.html', {'messages': get_messages_for_user(username), 'uuid': uuid})


def user_is_authenticated(request):
    return request.user.is_authenticated()


def get_already_registered_message(request):
    return render(request, 'register.html', {
        'messages': [{'msg_text': _("You're already logged in. Why don't you take our latest poll?")}],
        'is_complete': True})


def serve_post_response(request, uuid, ureporter):
    username = Ureporter.objects.get(uuid=uuid).urn_tel
    if request.POST.get('password'):
        activate_user(request, ureporter)
        send_message_to_rapidpro({'from': username, 'text': 'next'})
    else:
        send_message_to_rapidpro({'from': username, 'text': request.POST['send']})
    msgs = get_messages_for_user(username)
    return render(request, 'register.html', {
        'messages': msgs,
        'submission': request.POST.get('send') or None,
        'is_password': has_password_keyword(msgs, username),
        'uuid': uuid})
