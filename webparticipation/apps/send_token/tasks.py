from celery import task
from django.core.mail import EmailMessage


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
