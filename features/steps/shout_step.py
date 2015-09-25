from behave import *
import uuid as uuid
from django.contrib.auth.models import User
from page_actions import *
from page_objects import *


username = 'user999999999'
uid = uuid.uuid4()

email_address = 'ureport@webpro.com'
password = 'password'

@given(u'I am a logged into wep-pro')
def step_impl(context):
    login_to_web_pro(context, email_address, password)


@when(u'I visit the shout page')
def step_impl(context):
    go_to_shout_page(context)

@then(u'I shall be able to send a message')
def step_impl(context):
    send_a_message(context.browser, 'Testing Testing')
    assert (send_message_notification_present,'Thank_you_message not found')
