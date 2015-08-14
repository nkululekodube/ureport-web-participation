import os
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.rapidpro_receptor.views import send_message_to_rapidpro, get_messages_for_user


@login_required
def poll_response(request, poll_id):
    flow_uuid = get_flow_uuid_from_poll_id(request, poll_id)
    username = str(request.user)
    uuid = Ureporter.objects.get(user__username=username).uuid
    if request.method == 'GET':
        return serve_get_response(request, poll_id, flow_uuid, username, uuid)
    if request.method == 'POST':
        return serve_post_response(request, poll_id, flow_uuid, username)


def get_flow_uuid_from_poll_id(request, poll_id):
    # return '480047a3-e7de-488a-92ad-31480f1b9690'  # Sample Flow -  Simple Poll
    # return '06f8ce86-bd13-46ce-b828-8e2262178cef'  # Poll#19-World Hepatitis Day
    return '18e85fe7-1aaf-473a-b0a1-505fe38d6717'  # Breastfeeding Poll


def serve_get_response(request, poll_id, flow_uuid, username, uuid):
    if is_run_complete(flow_uuid, uuid):
        return serve_already_taken_poll_message(request, poll_id)
    trigger_flow_run(flow_uuid, uuid)
    messages = get_messages_for_user(username)
    return render(request, 'poll_response.html', {'messages': messages, 'poll_id': poll_id})


def is_run_complete(flow_uuid, uuid):
    return False
    api_path = os.environ.get('RAPIDPRO_API_PATH')
    rapidpro_api_token = os.environ.get('RAPIDPRO_API_TOKEN')
    runs = requests.get(api_path + '/runs.json?flow_uuid=' + flow_uuid + '&contacts=' + uuid,
                        headers={'Authorization': 'Token ' + rapidpro_api_token})
    return bool([run['completed'] for run in runs.json()['results'] if run['completed'] is True])


def serve_already_taken_poll_message(request, poll_id):
    return render(request, 'poll_response.html', {
        'messages': [{'msg_text': _("You've already taken this poll.")}],
        'poll_id': poll_id,
        'is_complete': True,
        'submission': request.POST.get('send')})


def trigger_flow_run(flow_uuid, uuid):
    api_path = os.environ.get('RAPIDPRO_API_PATH')
    rapidpro_api_token = os.environ.get('RAPIDPRO_API_TOKEN')
    requests.post(api_path + '/runs.json',
                  data={'flow_uuid': flow_uuid, 'contacts': uuid},
                  headers={'Authorization': 'Token ' + rapidpro_api_token})


def serve_post_response(request, poll_id, flow_uuid, username):
    send_message_to_rapidpro({'from': username, 'text': request.POST['send']})
    msgs = get_messages_for_user(username)
    return render(request, 'poll_response.html', {
        'messages': msgs,
        'poll_id': poll_id,
        'submission': request.POST.get('send')})
