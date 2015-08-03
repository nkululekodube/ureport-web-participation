from celery import task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
import os
from webparticipation.apps.login.models import PasswordReset


@task()
def send_forgot_password_email(email):
    try:
        user = User.objects.get(email=email)

        if user:
            expiry = timezone.now() + timezone.timedelta(days=settings.PASSWORD_RESET_EXPIRY_DAYS)
            password_reset = PasswordReset.build(expiry, user)
            password_reset.save()

            link = reset_password_url("/password-reset/%s" % password_reset.id)
            in_text = "<p>Please click this link to change " \
                      "your password on Ureport.in <a href='" + link + "'> Email reset link</a></p>"
            subject = 'Hi from ureport.in'

            body = in_text + '<p>-----Thanks</p>'
            signature = '\nureport team'
            recipients = [email]

            message = EmailMessage(subject, body + signature, to=recipients)
            message.content_subtype = "html"
            message.send()

    except User.DoesNotExist:
        print 'no user found'


def reset_password_url(path):
    protocol = "http"
    port = "8200"
    server_name = "127.0.0.1"
    return "%s://%s:%s/%s" % (protocol, server_name, port, path)

