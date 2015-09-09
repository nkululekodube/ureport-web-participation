from celery import task
from django.core.mail import EmailMessage
from webparticipation.apps.ureporter.models import delete_user_from_rapidpro as delete_from


@task()
def send_verification_token(ureporter):
    if ureporter.token:
        subject = 'Hello'
        body = 'Welcome to ureport. To complete the registration process, ' \
               'use this code to verify your account: ' + str(ureporter.token) + ' .' \
               '\n\n-----\nThanks'
        signature = '\nureport team'
        recipients = [ureporter.user.email]
        message = EmailMessage(subject, body + signature, to=recipients)
        message.send()


@task()
def delete_user_from_rapidpro(ureporter):
    delete_from(ureporter)
