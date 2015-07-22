from celery import task
from django.core.mail import EmailMessage
from webparticipation.apps.ureport_user.models import UreportUser


@task()
def send_verification_token(user):
    token = get_auth_token(user)
    if token:
        subject = 'Hello'
        body = 'Welcome to ureport. To complete the registration process, ' \
               'use this code to verify your account: ' + str(token) + ' .' \
               '\n\n-----\nThanks'
        signature = '\nureport team'
        recipients = [user.email]
        message = EmailMessage(subject, body + signature, to=recipients)
        message.send()


def get_auth_token(user_id):
    user = UreportUser.objects.get(uuid=user_id)
    token = user.token
    return token
