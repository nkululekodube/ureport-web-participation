import os
import json
import requests

from celery import task

from webparticipation.apps.latest_poll.models import LatestPoll


@task(name='latest_poll.retrieve_latest_poll')
def retrieve_latest_poll():
    response = requests.get(os.environ.get('UREPORT_ROOT') +
                            '/api/poll/latest/' + os.environ.get('UREPORT_ORG_ID') + '/')
    latest_poll_id = json.loads(response.content)['poll_id']
    lastest_poll_singleton = LatestPoll.get_solo()
    lastest_poll_singleton.poll_id = latest_poll_id
    lastest_poll_singleton.save()
