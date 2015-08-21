import os
import json
import requests

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from celery import task

from webparticipation.apps.latest_poll.models import LatestPoll


@task(name='latest_poll.retrieve_latest_poll')
def retrieve_latest_poll():
    response = requests.get(os.environ.get('UREPORT_ROOT') +
                            '/api/poll/latest/' + os.environ.get('UREPORT_ORG_ID') + '/')
    latest_poll_id = json.loads(response.content)['poll_id']
    lastest_poll_singleton = LatestPoll.get_solo()
    if lastest_poll_singleton != latest_poll_id:
        lastest_poll_singleton.poll_id = latest_poll_id
        lastest_poll_singleton.save()
        notify_users_of_new_poll(latest_poll_id)


def notify_users_of_new_poll(latest_poll_id):
    flow_info = requests.get(os.environ.get('UREPORT_ROOT') + '/api/flow/' + str(latest_poll_id) + '/')
    flow_info_dict = json.loads(flow_info.content)

    subject = 'New Ureport poll "' + flow_info_dict['title'] + '" now available'

    body = 'Hello Ureporter,' + '\n\n'\
           'We have published a new poll, "' + flow_info_dict['title'] + '". ' + \
           'Take the poll by clicking the link below:' + '\n' + \
           os.environ.get('WEBPARTICIPATION_ROOT') + '/poll/' + str(latest_poll_id) + '/respond/' + '\n\n' \
           '-----'
    signature = '\nYour friendly Ureport team'
    active_users = User.objects.filter(is_active=True)
    recipients = [user.email for user in active_users]
    message = EmailMessage(subject, body + signature, bcc=recipients)
    message.send()
