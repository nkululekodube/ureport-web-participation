import requests

from django.shortcuts import render
from django.conf import settings as s
from django.utils.translation import ugettext as _

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
        send_message_to_rapidpro({'from': username, 'text': s.RAPIDPRO_REGISTER_TRIGGER})

        return render(request, 'register.html', {
            'messages': get_messages_for_user(username),
            'uuid': reporter.uuid,
            'run_id': get_run_id(reporter)})


def user_is_authenticated(request):
    return request.user.is_authenticated()


def get_run_id(reporter):
    query_path = '%s/runs.json?flow_uuid=%s&contact=%s' % (
        s.RAPIDPRO_API_PATH, s.UREPORT_REGISTRATION_FLOW_UUID, reporter.uuid)
    run = requests.get(query_path, headers={'Authorization': 'Token ' + s.RAPIDPRO_API_TOKEN}).json()
    run_id = run['results'][0]['run']
    return run_id


def get_already_registered_message(request):
    return render(request, 'register.html', {
        'messages': [_("You're already logged in. Why don't you take our latest poll?")],
        'is_complete': True})


def serve_post_response(request, reporter):
    username = reporter.urn_tel
    run_id = request.POST['run_id']

    if request.POST.get('password'):
        activate_user(request, reporter)
        send_message_to_rapidpro({'from': username, 'text': 'next'})
    else:
        send_message_to_rapidpro({'from': username, 'text': request.POST['send']})

    msgs = get_messages_for_user(username)
    if False in msgs:
        return serve_timeout_message(request, msgs)

    is_password = has_password_keyword(msgs, username)
    post_password = get_post_password_status(request, is_password)
    show_latest_poll_link = post_password > ON_PASSWORD
    is_complete = is_registration_complete(run_id)

    return render(request, 'register.html', {
        'is_complete': is_complete,
        'messages': msgs,
        'submission': request.POST.get('send') or None,
        'is_password': is_password,
        'post_password': post_password,
        'show_latest_poll_link': show_latest_poll_link,
        'uuid': reporter.uuid,
        'run_id': run_id})


def is_registration_complete(run_id):
    query_path = '%s/runs.json?flow_uuid=%s&run=%s' % (
        s.RAPIDPRO_API_PATH, s.UREPORT_REGISTRATION_FLOW_UUID, run_id)
    run = requests.get(query_path, headers={'Authorization': 'Token ' + s.RAPIDPRO_API_TOKEN}).json()
    is_complete = run['results'][0]['completed']
    return is_complete


def serve_timeout_message(request, msgs):
    msgs = msgs[0]
    return render(request, 'register.html', {
        'messages': msgs,
        'is_complete': True,
        'submission': request.POST.get('send')})


def get_post_password_status(request, is_password):
    post_password = request.POST['post_password'] or BEFORE_PASSWORD
    if int(post_password) == ON_PASSWORD:
        post_password = POST_PASSWORD
    if is_password:
        post_password = ON_PASSWORD
    return post_password
