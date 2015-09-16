from celery import task

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone

from webparticipation.apps.utils.views import get_url
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
            except PasswordReset.DoesNotExist:
                password_reset = PasswordReset.objects.create(expiry=expiry, user=user)
                password_reset.generate_password_reset_token()

            subject = 'Ureport Password Recovery'
            email_content = construct_forgotten_password_email(password_reset)
            recipients = [email]
            message = EmailMessage(subject, email_content, to=recipients)
            message.content_subtype = 'html'
            message.send()
    except User.DoesNotExist:
        print 'no user found'


def construct_forgotten_password_email(password_reset):
    link = get_url('/password-reset/%s/' % password_reset.token)
    unsubscribe_link = get_url('/ureporter/unsubscribe/')
    body = '<p>Hello from Ureport,</p>' \
           '<p>You recently requested a reset of your ureport account password.</p>' \
           '<p>To do this, please click this password recovery link to change your password: ' + link + '</p>'\
           '<p>-----</p>' \
           '<p>Thanks,</p>'
    signature = '<p>Your friendly Ureport team</p>'
    footer = '<hr>' \
             '<p>Please click <a href="' + unsubscribe_link + '">unsubscribe</a> ' \
             'to stop receiving email notifications</p>'
    return '%s%s%s' % (body, signature, footer)
