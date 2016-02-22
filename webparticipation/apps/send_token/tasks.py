from celery import task
from django.core.mail import EmailMessage
from webparticipation.apps.ureporter.models import delete_user_from_rapidpro as delete_from


@task()
def send_verification_token(ureporter):
    if ureporter.token:
        subject = 'U-Report Registration'
        body = 'Thank you for registering with U-Report. ' \
               'Here is your code to complete your U-Report profile: ' + str(ureporter.token) + ' .' \
               '\n\nWe are so happy for you to join us to speak out on the important issues ' \
               'affecting young people in your community.'
        signature = '\n\n-----\nU-Report\nVoice Matters' \
                    '\n\nThis is an automated email so please don\'t reply.' \
                    '\nFor more information about U-Report go to www.ureport.in/about ' \
                    'or follow us on Twitter @UReportGlobal'
        recipients = [ureporter.user.email]
        message = EmailMessage(subject, body + signature, to=recipients)
        message.send()


@task()
def delete_user_from_rapidpro(ureporter):
    delete_from(ureporter)
