from celery import task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from webparticipation.apps.login.models import PasswordReset
from webparticipation.apps.ureporter.models import Ureporter


@task()
def send_forgot_password_email(email):
    try:
        user = User.objects.get(email=email)

        if user:
            expiry = timezone.now() + timezone.timedelta(days=settings.PASSWORD_RESET_EXPIRY_DAYS)
            password_reset = PasswordReset.build(expiry, user)
            password_reset.save()

            uuid = Ureporter.objects.get(user_id=password_reset.user_id).uuid

            link = reset_password_url("/password-reset/%s" % uuid)
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
    return "%s%s:%s%s" % (settings.ENV_PROTOCOL,
                          settings.ENV_SERVER_NAME,
                          settings.ENV_PORT, path)
