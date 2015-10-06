from django.core.urlresolvers import reverse
import requests
from celery import task
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from webparticipation.apps.utils.views import get_url
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.latest_poll.models import LatestPoll


@task(name='latest_poll.retrieve_latest_poll')
def retrieve_latest_poll():
    response = requests.get(settings.UREPORT_ROOT +
                            '/api/v1/polls/org/' + settings.UREPORT_ORG_ID + '/featured/?format=json').json()
    latest_poll_id_from_api = response['results'][0]['id']
    latest_poll_id_flow_uuid = response['results'][0]['flow_uuid']
    latest_poll_singleton = LatestPoll.get_solo()
    if latest_poll_singleton.flow_uuid == '':
        latest_poll_singleton.flow_uuid = latest_poll_id_flow_uuid
        latest_poll_singleton.save()
    if not latest_poll_singleton.poll_id == latest_poll_id_from_api \
            and not latest_poll_singleton.has_in_previous_featured_polls(latest_poll_id_from_api):
        latest_poll_singleton.set_poll_id(latest_poll_id_from_api, latest_poll_id_flow_uuid)
        latest_poll_singleton.add_featured_poll(latest_poll_id_from_api)
        notify_users_of_new_poll(latest_poll_id_from_api)


def notify_users_of_new_poll(latest_poll_id):
    flow_info = requests.get(settings.UREPORT_ROOT + '/api/v1/polls/' + str(latest_poll_id) + '/').json()

    subject = _('New U-Report poll %s now available' % flow_info['title'])

    active_users = Ureporter.objects \
        .filter(user__is_active=True, subscribed=True) \
        .exclude(last_poll_taken=latest_poll_id)
    for reporter in active_users:
        email_content = construct_new_poll_email(flow_info, latest_poll_id, reporter)
        message = EmailMessage(subject, email_content, to=[reporter.user.email])
        message.content_subtype = 'html'
        message.send()


def construct_new_poll_email(flow_info, latest_poll_id, reporter):
    unsubscribe_path = reverse("unsubscribe", kwargs={"unsubscribe_token": reporter.unsubscribe_token})
    unsubscribe_link = get_url(unsubscribe_path)
    body = '<p>Hello U-Reporter,</p>' \
           '<p>We have published a new poll, "' + flow_info['title'] + '".</p>' \
                                                                       '<p>Take the poll by clicking the following link: ' + \
           settings.WEBPARTICIPATION_ROOT + '/poll/' + str(latest_poll_id) + '/respond/</p>' \
                                                                             '<p>-----</p>'
    signature = '<p>Your friendly U-Report team</p>'
    footer = '<hr>' \
             '<p>Please click <a href="' + unsubscribe_link + '">unsubscribe</a> ' \
                                                              'to stop receiving email notifications</p>'
    return '%s%s%s' % (body, signature, footer)
