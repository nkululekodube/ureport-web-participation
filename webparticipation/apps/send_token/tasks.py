from celery import task
from django.core.mail import EmailMessage


@task()
def send_verification_token(user):
    if user.token:
        subject = 'Hello'
        body = 'Welcome to ureport. To complete the registration process, ' \
               'use this code to verify your account: ' + str(user.token) + ' .' \
               '\n\n-----\nThanks'
        signature = '\nureport team'
        recipients = [user.email]
        message = EmailMessage(subject, body + signature, to=recipients)
        message.send()
