from behave import *
import time
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from webparticipation.apps.ureport_auth.models import PasswordReset

username = 'user999999999'
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
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(1)
    print(User.objects.get(email='mben03@gmail.com').__dict__, "Then User input \n")

@then(u'I shall see a notification \'We have sent an email ...\'')
def step_impl(context):
    time.sleep(2)
    assert context.browser.is_text_present('We have sent an email to mben03@gmail.com'), 'Email notification not found'

@then(u'I shall input a wrong email address')
def step_impl(context):
    time.sleep(2)
    context.browser.fill('email', 'test@gmail.com')
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I shall see a notification \'There is no registered user ... \'')
def step_impl(context):
    time.sleep(2)
    assert context.browser.is_text_present('There is no registered user'), 'No registered user notification not found'

@when(u'I see the page requesting me for an email address')
def step_impl(context):
    # pass
    time.sleep(2)
    assert context.browser.find_by_name('email'), 'Email field not found'

@when(u'I shall input my email address')
def step_impl(context):
    pass
    time.sleep(2)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(1)
    user = User.objects.get(username=username)
    print(user.__dict__, "User \n")

@when(u'I shall see a notification \'We have sent an email ...\'')
def step_impl(context):
    # pass
    time.sleep(2)
    assert context.browser.is_text_present('We have sent an email to mben03@gmail.com'), 'Email notification not found'

@when(u'I go to reset password page')
def step_impl(context):
    time.sleep(2)
    user = User.objects.get(username=username)
    PasswordReset.objects.create(expiry=expiry, user=user, token=uuid.uuid4().hex)
    password_reset = PasswordReset.objects.all()[0]
    url = context.base_url + '/password-reset/' + str(password_reset.token)
    print(password_reset.token, "Reset Password - token \n")
    print(url, "URL \n")
    print(password_reset.__dict__, "Reset Password \n")
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
    pass

@then(u'I shall login with the new password')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'Password1')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'
    context.browser.find_link_by_href('/logout/').click()

@when(u'I visit reset password page')
def step_impl(context):
    time.sleep(2)
    user = User.objects.get(username=username)
    PasswordReset.objects.create(expiry=expiry, user=user, token=uuid.uuid4().hex)
    password_reset = PasswordReset.objects.all()[0]
    url = context.base_url + '/password-reset/' + str(password_reset.token)
    print(password_reset.token, "Reset Password - token \n")
    print(url, "URL \n")
    print(password_reset.__dict__, "Reset Password \n")
    context.browser.visit(url)
    time.sleep(2)

@when(u'I submit my un matching passwords')
def step_impl(context):
    time.sleep(1)
    print(context.browser.url)
    context.browser.fill('password', 'Password1')
    context.browser.fill('confirm_password', 'Password2')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I see a notification of passwords do not match')
def step_impl(context):
    pass

@then(u'I shall login with the old password')
def step_impl(context):
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'password')
    time.sleep(2)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'
    context.browser.find_link_by_href('/logout/').click()