from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.conf import settings

from webparticipation.apps.ureporter.views import get_user, activate_user
from webparticipation.apps.rapidpro_receptor.views import send_message_to_rapidpro, has_password_keyword, \
    get_messages_for_user

POST_PASSWORD = 2

ON_PASSWORD = 1

BEFORE_PASSWORD = 0


def register(request):
    reporter = get_user(request)
    if request.method == 'GET':
        return serve_get_response(request, reporter)
    if request.method == 'POST':
        return serve_post_response(request, reporter)


def serve_get_response(request, reporter):
    username = reporter.urn_tel
    if user_is_authenticated(request):
        return get_already_registered_message(request)
    else:
        send_message_to_rapidpro({'from': username, 'text': settings.RAPIDPRO_REGISTER_TRIGGER})
        return render(request, 'register.html', {'messages': get_messages_for_user(username), 'uuid': reporter.uuid})


def user_is_authenticated(request):
    return request.user.is_authenticated()


def get_already_registered_message(request):
    return render(request, 'register.html', {
        'messages': [_("You're already logged in. Why don't you take our latest poll?")],
        'is_complete': True})


def serve_post_response(request, reporter):
    username = reporter.urn_tel
    if request.POST.get('password'):
        activate_user(request, reporter)
        send_message_to_rapidpro({'from': username, 'text': 'next'})
    else:
        send_message_to_rapidpro({'from': username, 'text': request.POST['send']})
    msgs = get_messages_for_user(username)
    is_password = has_password_keyword(msgs, username)
    post_password = get_post_password_status(request, is_password)
    show_latest_poll_link = post_password > ON_PASSWORD
    return render(request, 'register.html', {
        'messages': msgs,
        'submission': request.POST.get('send') or None,
        'is_password': is_password,
        'post_password': post_password,
        'show_latest_poll_link': show_latest_poll_link,
        'uuid': reporter.uuid})


def get_post_password_status(request, is_password):
    post_password = request.POST['post_password'] or BEFORE_PASSWORD  # 0=before password, 1=on password, 2=post password
    if int(post_password) == ON_PASSWORD:
        post_password = POST_PASSWORD
    if is_password:
        post_password = ON_PASSWORD
    return post_password
