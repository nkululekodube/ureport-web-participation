from behave import *
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from webparticipation.apps.ureport_auth.models import PasswordReset

from page_actions import *
from page_objects import *

username = 'user999999999'
user_email = 'ureport@webpro.com'
password = 'Password1'
test_email = 'test@gmail.com'

expiry = timezone.now() + timezone.timedelta(days=1)

@when(u'I click Forgot-password link')
def step_impl(context):
    context.browser.find_link_by_href('/forgot-password/').click()
    time.sleep(2)

@then(u'I see the page requesting me for an email address')
def step_impl(context):
    time.sleep(2)
    assert context.browser.find_by_name('email'), 'Email field not found'


@then(u'I shall input my email address')
def step_impl(context):
    send_forgot_password_email(context.browser, user_email)

@then(u'I shall see a notification \'We have sent an email ...\'')
def step_impl(context):
    time.sleep(1)
    assert sent_email_notification_present(context.browser,user_email), 'Email notification not found'
    time.sleep(1)

@then(u'I shall input a wrong email address')
def step_impl(context):
    time.sleep(2)
    send_forgot_password_email(context.browser, test_email)

@then(u'I shall see a notification \'There is no registered user ... \'')
def step_impl(context):
    time.sleep(1)
    assert no_user_notification_present(context.browser, test_email), 'No registered user notification not found'
    time.sleep(1)

@when(u'I see the page requesting me for an email address')
def step_impl(context):
    time.sleep(1)
    assert email_input_field(context.browser), 'Email field not found'
    time.sleep(1)

@when(u'I shall input my email address')
def step_impl(context):
    send_forgot_password_email(context.browser, user_email)
    assert sent_email_notification_present(context.browser, user_email), 'Email notification not found'

@when(u'I go to reset password page')
def step_impl(context):
    time.sleep(2)
    user = User.objects.get(email=user_email)
    password_reset = PasswordReset.objects.create(expiry=expiry, user=user, token=uuid.uuid4().hex)
    url = context.base_url + '/password-reset/' + str(password_reset.token)
    context.browser.visit(url)
    time.sleep(2)

@then(u'I shall change my password')
def step_impl(context):
    reset_password(context.browser, password='Password1', confirm_password='Password1')
    time.sleep(2)
    assert password_changed_notification_present(context.browser, user_email), 'password_changed not found'


@then(u'I shall login with the new password')
def step_impl(context):
    login_to_web_pro(context, user_email, password)
    assert logout_link(context.browser), 'Logout link not found'
    logout_link(context.browser).click()

@when(u'I visit reset password page')
def step_impl(context):
    time.sleep(2)
    user = User.objects.get(email=user_email)
    password_reset = PasswordReset.objects.create(expiry=expiry, user=user, token=uuid.uuid4().hex)
    url = context.base_url + '/password-reset/' + str(password_reset.token)
    context.browser.visit(url)
    time.sleep(2)

@when(u'I submit my un matching passwords')
def step_impl(context):
    reset_password(context.browser, password='Password1', confirm_password='Password2')

@then(u'I see a notification of passwords do not match')
def step_impl(context):
    time.sleep(2)
    assert password_unmatched_notification_present(context.browser), 'passwords-do-not-match not found'

@then(u'I shall login with the old password')
def step_impl(context):
    login_to_web_pro(context, user_email, password='password')
    log_out_of_web_pro(context)
