from celery import task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from webparticipation.apps.ureport_auth.models import PasswordReset
from webparticipation.apps.ureporter.models import Ureporter
import os


@task()
def send_forgot_password_email(email):
    try:
        user = User.objects.get(email=email)
        if user:
            expiry = timezone.now() + timezone.timedelta(days=settings.PASSWORD_RESET_EXPIRY_DAYS)
            password_reset = PasswordReset.build(expiry, user)
            password_reset.save()
            uuid = Ureporter.objects.get(user_id=password_reset.user_id).uuid

            link = reset_password_url('/password-reset/%s' % uuid)
            subject = 'Hi from ureport.in'
            html_text = "<p>" + subject + "<p>You recently requested to reset your ureport account password.</p> " \
                                          "<p>To do this, please click this password link to change " \
                                          "your password <a href='" + link + "'>  Password recovery link</a></p>"

            body = html_text + '<p>-----</p><p>Thanks</p>'
            signature = '\nureport team'
            recipients = [email]

            message = EmailMessage('Ureport Password Recovery', body + signature, to=recipients)
            message.content_subtype = "html"
            message.send()

    except User.DoesNotExist:
        print 'no user found'


def reset_password_url(path):
    return '%s%s' % (os.environ.get('WEBPARTICIPATION_ROOT'), path)
