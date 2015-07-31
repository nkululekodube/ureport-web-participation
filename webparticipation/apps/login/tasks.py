from celery import task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


@task()
def send_forgot_password_email(email):
    message = ''

    try:
        user = User.objects.get(email=email)
        if user:
            link = 'link_url'
            message = "Please click this link to change " \
                      "your password on Ureport.in %s", link
    except User.DoesNotExist:
        message = "Someone has requested that the password for this" \
                  "email address be reset, " \
                  "however we don't have an account associated with it.\n " \
                  "If you did not request this, " \
                  "don't worry, this email has only been " \
                  "sent to you and your account remains secure."

    subject = 'Hi from ureport.in'
    body = message + '\n\n-----\nThanks'
    signature = '\nureport team'
    recipients = [email]
    message = EmailMessage(subject, body + signature, to=recipients)
    message.send()
