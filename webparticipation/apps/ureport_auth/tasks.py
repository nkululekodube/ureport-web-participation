from celery import task

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from webparticipation.apps.utils.views import get_url
from webparticipation.apps.ureport_auth.models import PasswordReset
from webparticipation.apps.ureporter.models import Ureporter


@task()
def send_forgot_password_email(email):
    user = User.objects.filter(email=email).first()
    if user:
        expiry = timezone.now() + timezone.timedelta(days=settings.PASSWORD_RESET_EXPIRY_DAYS)
        password_reset = PasswordReset.objects.filter(user_id=user.id).first()
        if password_reset:
            password_reset.set_expiry(expiry)
            password_reset.generate_password_reset_token()
        else:
            password_reset = PasswordReset.objects.create(expiry=expiry, user=user)
            password_reset.generate_password_reset_token()

        subject = _('Ureport Password Recovery')
        email_content = construct_forgotten_password_email(email)
        recipients = [email]
        message = EmailMessage(subject, email_content, to=recipients)
        message.content_subtype = 'html'
        message.send()


def construct_forgotten_password_email(email):
    ureporter = Ureporter.objects.get(user__email=email)
    password_reset = PasswordReset.objects.get(user_id=ureporter.user.id)
    password_reset_link = get_url('/password-reset/%s/' % password_reset.token)
    unsubscribe_link = get_url('/profile/unsubscribe/%s' % ureporter.unsubscribe_token)
    body = '<p>Hello from Ureport,</p>' \
           '<p>You recently requested a reset of your ureport account password.</p>' \
           '<p>To do this, please click this password recovery link to change your password: %s</p>'\
           '<p>-----</p>' \
           '<p>Thanks,</p>' % password_reset_link
    signature = _('<p>Your friendly Ureport team</p>')
    footer = '<hr>' \
             '<p>Please click <a href="%s">unsubscribe</a> ' \
             'to stop receiving email notifications</p>' % unsubscribe_link
    return '%s%s%s' % (body, signature, footer)
