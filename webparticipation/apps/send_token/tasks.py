from celery import task
from django.core.mail import EmailMessage
import binascii
import random
import string


@task()
def send_verification_token(user):
    subject = 'Hello'
    body = 'Welcome to ureport. To complete the registration process, ' \
           'use this code to verify your account ' + generate_auth_token() + ' .' \
                                                                             '\n\n-----\nThanks'
    signature = '\nureport team'
    recipients = [user.email]
    message = EmailMessage(subject, body + signature, to=recipients)
    message.send()


def generate_auth_token():
    digits = string.digits
    return binascii.hexlify(''.join([random.choice(digits) for _ in range(4)]))
