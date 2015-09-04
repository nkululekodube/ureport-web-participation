import os

from celery import task

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from webparticipation.apps.ureport_auth.models import PasswordReset


@task()
def send_forgot_password_email(email):
    try:
        user = User.objects.get(email=email)
        if user:
            expiry = timezone.now() + timezone.timedelta(days=settings.PASSWORD_RESET_EXPIRY_DAYS)
            try:
                password_reset = PasswordReset.objects.get(user_id=user.id)
                if password_reset:
                    password_reset.set_expiry(expiry)
                    password_reset.generate_password_reset_token()
                    # link = reset_password_url('/password-reset/%s' % password_reset.token)
            except PasswordReset.DoesNotExist:
                password_reset = PasswordReset.objects.create(expiry=expiry, user=user)
                password_reset.generate_password_reset_token()

            link = reset_password_url('/password-reset/%s' % password_reset.token)

            subject = 'Hi from ureport.in'
            html_text = "<p>" + subject + "</p>" \
                                          "<p>You recently requested to reset your ureport account password.</p>" \
                                          "<p>To do this, please click this password link to change your password " \
                                          "<a href='" + link + "'>Password recovery link</a></p>"
            body = html_text + '<p>------</p>' \
                               '<p>Thanks</p>'
            signature = '\nureport team'
            recipients = [email]

            message = EmailMessage('Ureport Password Recovery', body + signature, to=recipients)
            message.content_subtype = 'html'
            message.send()

    except User.DoesNotExist:
        print 'no user found'


def reset_password_url(path):
    return '%s%s' % (settings.WEBPARTICIPATION_ROOT, path)
