import requests
from django.core.mail import EmailMessage
from django.conf import settings
from celery import task

from webparticipation.apps.utils.views import get_url
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.latest_poll.models import LatestPoll


@task(name='latest_poll.retrieve_latest_poll')
def retrieve_latest_poll():
    response = requests.get(settings.UREPORT_ROOT +
                            '/api/v1/polls/org/' + settings.UREPORT_ORG_ID + '/featured/?format=json').json()
    latest_poll_id_from_api = response['results'][0]['id']
    latest_poll_singleton = LatestPoll.get_solo()
    if not latest_poll_singleton.poll_id == latest_poll_id_from_api \
       and not latest_poll_singleton.has_in_previous_featured_polls(latest_poll_id_from_api):
        latest_poll_singleton.set_poll_id(latest_poll_id_from_api)
        latest_poll_singleton.add_featured_poll(latest_poll_id_from_api)
        notify_users_of_new_poll(latest_poll_id_from_api)


def notify_users_of_new_poll(latest_poll_id):
    flow_info = requests.get(settings.UREPORT_ROOT + '/api/v1/polls/' + str(latest_poll_id) + '/').json()

    subject = 'New Ureport poll "' + flow_info['title'] + '" now available'
    email_content = construct_new_poll_email(flow_info, latest_poll_id)

    active_users = Ureporter.objects \
                            .filter(user__is_active=True, subscribed=True) \
                            .exclude(last_poll_taken=latest_poll_id)
    recipients = [user.user.email for user in active_users]

    message = EmailMessage(subject, email_content, bcc=recipients)
    message.content_subtype = 'html'
    message.send()
    return message


def construct_new_poll_email(flow_info, latest_poll_id):
    unsubscribe_link = get_url('/ureporter/unsubscribe/')
    body = '<p>Hello Ureporter,</p>' \
           '<p>We have published a new poll, "' + flow_info['title'] + '".</p>' \
           '<p>Take the poll by clicking the following link: ' + \
           settings.WEBPARTICIPATION_ROOT + '/poll/' + str(latest_poll_id) + '/respond/</p>' \
           '<p>-----</p>'
    signature = '<p>Your friendly Ureport team</p>'
    footer = '<hr>' \
             '<p>Please click <a href="' + unsubscribe_link + '">unsubscribe</a> ' \
             'to stop receiving email notifications</p>'
    return '%s%s%s' % (body, signature, footer)
