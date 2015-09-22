from django.conf import settings
import requests


def get_runs_for_ureporter(reporter):
    params = {'contact': reporter.uuid}
    headers = {'Authorization': 'Token %s' % settings.RAPIDPRO_API_TOKEN}
    url = '%s/runs.json' % settings.RAPIDPRO_API_PATH
    return requests.get(url, params=params, headers=headers).json()


def get_poll_id(flow_id):
    url = '%s/api/v1/polls/org/%s/' % (settings.UREPORT_ROOT, settings.UREPORT_ORG_ID)
    params = {'flow_uuid': flow_id}
    try:
        data = requests.get(url, params=params).json()
        if len(data['results']) > 0:
            return data['results'][0]['id']
    except requests.exceptions.RequestException as e:
        print e
        pass

    return None