from behave import *
import time
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from webparticipation.apps.ureport_auth.models import PasswordReset

username = 'user999999999'
user_email = 'ureport@webpro.com'
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
    time.sleep(2)
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(2)

@then(u'I shall see a notification \'We have sent an email ...\'')
def step_impl(context):
    time.sleep(1)
    assert context.browser.is_text_present('We have sent an email to ureport@webpro.com'), 'Email notification not found'
    time.sleep(1)

@then(u'I shall input a wrong email address')
def step_impl(context):
    time.sleep(2)
    context.browser.fill('email', 'test@gmail.com')
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I shall see a notification \'There is no registered user ... \'')
def step_impl(context):
    time.sleep(1)
    assert context.browser.is_text_present('There is no registered user'), 'No registered user notification not found'
    time.sleep(1)

@when(u'I see the page requesting me for an email address')
def step_impl(context):
    time.sleep(1)
    assert context.browser.find_by_name('email'), 'Email field not found'
    time.sleep(1)

@when(u'I shall input my email address')
def step_impl(context):
    time.sleep(2)
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(1)
    user = User.objects.get(email=user_email)

@when(u'I shall see a notification \'We have sent an email ...\'')
def step_impl(context):
    time.sleep(2)
    assert context.browser.is_text_present('We have sent an email to ureport@webpro.com'), 'Email notification not found'

@when(u'I go to reset password page')
def step_impl(context):
    time.sleep(2)
    user = User.objects.get(email=user_email)
    password_reset = PasswordReset.objects.create(expiry=expiry, user=user, token=uuid.uuid4().hex)
    url = context.base_url + '/password-reset/' + str(password_reset.token)
    context.browser.visit(url)
    time.sleep(2)

@then(u'I submit my new password')
def step_impl(context):
    time.sleep(2)
    context.browser.fill('password', 'Password1')
    context.browser.fill('confirm_password', 'Password1')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I see a notification of password changed')
def step_impl(context):
    time.sleep(2)
    assert context.browser.is_text_present('Password successfully changed for ureport@webpro.com'), 'password_changed not found'


@then(u'I shall login with the new password')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.fill('password', 'Password1')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'
    context.browser.find_link_by_href('/logout/').click()

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
    time.sleep(1)
    context.browser.fill('password', 'Password1')
    context.browser.fill('confirm_password', 'Password2')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I see a notification of passwords do not match')
def step_impl(context):
    time.sleep(2)
    assert context.browser.is_text_present('Password do not match'), 'passwords-do-not-match not found'

@then(u'I shall login with the old password')
def step_impl(context):
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.fill('password', 'password')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'
    context.browser.find_link_by_href('/logout/').click()