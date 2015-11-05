import datetime
import json
from time import sleep

import requests
from django.conf import settings as s
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext as _

from webparticipation.apps.rapidpro_receptor.views import send_message_to_rapidpro, get_messages_for_user
from webparticipation.apps.ureporter.models import Ureporter


@login_required
def poll_response(request, poll_id):
    if request.method == 'GET':
        return serve_get_response(request, poll_id)
    if request.method == 'POST':
        return serve_post_response(request, poll_id)


@login_required
def latest_poll_response(request):
    featured_poll = requests.get(s.UREPORT_ROOT + '/api/v1/polls/org/' + s.UREPORT_ORG_ID + '/featured/').json()
    if featured_poll['count']:
        latest_poll_id = featured_poll['results'][0]['id']
        return poll_response(request, latest_poll_id)
    else:
        return render_no_current_poll_available(request)


def render_no_current_poll_available(request):
    return render(request, 'poll_response.html', {
        'messages': [{'msg_text': _('There is no current poll available.')}],
        'is_complete': True,
        'no_latest': True,
        'submission': request.POST.get('send')})


def serve_get_response(request, poll_id):
    username = request.user
    uuid = Ureporter.objects.get(user__username=username).uuid
    flow_info = get_flow_info_from_poll_id(request, poll_id)

    if complete_run_already_exists(flow_info['flow_uuid'], uuid):
        return render_already_taken_poll_message(request, poll_id, flow_info)

    run = trigger_flow_run(flow_info['flow_uuid'], uuid)
    run_id = run.json()[0]['run']

    messages = get_messages_for_user(username)

    return render(request, 'poll_response.html',
                  {'messages': messages,
                   'poll_id': poll_id,
                   'title': flow_info['title'],
                   'flow_info': json.dumps(flow_info),
                   'run_id': run_id})


def get_flow_info_from_poll_id(request, poll_id):
    flow_info = requests.get(s.UREPORT_ROOT + '/api/v1/polls/' + str(poll_id) + '/').json()
    return flow_info


def complete_run_already_exists(flow_uuid, uuid):
    query_path = '%s/runs.json?flow_uuid=%s&contact=%s' % (s.RAPIDPRO_API_PATH, flow_uuid, uuid)
    runs = requests.get(query_path, headers={'Authorization': 'Token ' + s.RAPIDPRO_API_TOKEN}).json()
    return has_completed_run(runs.get('results', []))


def has_completed_run(run_results):
    return any([run.get('completed', False) for run in run_results])


def render_already_taken_poll_message(request, poll_id, flow_info):
    return render(request, 'poll_response.html', {
        'messages': [_("You've already taken this poll.")],
        'title': flow_info['title'],
        'is_complete': True})


def trigger_flow_run(flow_uuid, uuid):
    run = requests.post(s.RAPIDPRO_API_PATH + '/runs.json',
                        data={'flow_uuid': flow_uuid, 'contacts': uuid},
                        headers={'Authorization': 'Token ' + s.RAPIDPRO_API_TOKEN})
    return run


def serve_post_response(request, poll_id):
    username = request.user
    uuid = Ureporter.objects.get(user__username=username).uuid
    flow_info = json.loads(request.POST['flow_info'])
    run_id = request.POST['run_id']
    send_message_to_rapidpro({'from': username, 'text': request.POST['send']})
    run_is_complete = is_current_run_complete(flow_info['flow_uuid'], uuid, run_id)
    if run_is_complete:
        msgs = ["Poll Completed"]
    else:
        msgs = get_messages_for_user(username)
    if False in msgs and not run_is_complete:
        return render_timeout_message(request, msgs)
    else:
        if run_is_complete:
            ureporter = Ureporter.objects.get(user__username=username)
            ureporter.set_last_poll_taken(poll_id)
        return render(request, 'poll_response.html', {
            'messages': msgs,
            'poll_id': poll_id,
            'flow_info': json.dumps(flow_info),
            'title': flow_info['title'],
            'run_id': run_id,
            'is_complete': run_is_complete,
            'submission': request.POST.get('send')})


def current_datetime_to_rapidpro_formatted_date():
    return (datetime.datetime.utcnow() - datetime.timedelta(seconds=int(s.UREPORT_TIME_DELTA))) \
               .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def is_current_run_complete(flow_uuid, uuid, run_id):
    start_time = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=10)
    while True:
        time_now = datetime.datetime.now()
        if time_now > start_time + timeout:
            return False
        user_run_query_path = '%s/runs.json?flow_uuid=%s&contact=%s&run=%s' \
                              % (s.RAPIDPRO_API_PATH, flow_uuid, uuid, str(run_id))
        user_run = requests.get(user_run_query_path, headers={'Authorization': 'Token ' + s.RAPIDPRO_API_TOKEN}).json()
        if user_run['count'] > 0:
            user_run_has_values = bool(user_run['results'][0]['values'])
            if not user_run_has_values:
                return False
            results = user_run['results']
            return has_completed_run(results)
        else:
            sleep(2)


def get_last_value_time(user_run):
    return user_run['results'][0]['values'][-1::][0]['time']


def render_timeout_message(request, msgs):
    flow_info = json.loads(request.POST['flow_info'])
    msgs = msgs[0]
    return render(request, 'poll_response.html', {
        'messages': msgs,
        'title': flow_info['title'],
        'poll_id': flow_info['id'],
        'is_complete': True,
        'timeout': True,
        'submission': request.POST.get('send')})
