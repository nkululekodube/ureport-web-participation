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

            link = reset_password_url("/reset-password/%s" % password_reset.id)
            message = "Please click this link to change " \
                      "your password on Ureport.in " + link
            subject = 'Hi from ureport.in'
            body = message + '\n\n-----\nThanks'
            signature = '\nureport team'
            recipients = [email,]

            message = EmailMessage(subject, body + signature, to=recipients)
            print message
            message.send()
    except User.DoesNotExist:
        print 'no user found'


def reset_password_url(path):
    return "%s://%s/%s" % (os.environ.get('RAPIDPRO_PROTOCOL'), os.environ.get('RAPIDPRO_HOST'), path)
