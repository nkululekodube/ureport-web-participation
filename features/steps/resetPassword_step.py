from behave import *
import time
from django.utils import timezone
from django.contrib.auth.models import User
from webparticipation.apps.ureport_auth.models import PasswordReset

import uuid

username = 'user999999999'
expiry = timezone.now() + timezone.timedelta(days=1)

@when(u'I change visit reset password page')
def step_impl(context):
    user = User.objects.get(username=username)
    PasswordReset.objects.create(expiry=expiry, user=user, token=uuid.uuid4().hex)
    password_reset = PasswordReset.objects.get(user=user)
    # print(PasswordReset.objects.get(user=user).__dict__)
    context.browser.visit('http://localhost:4000/password-reset/' + password_reset.token)


@when(u'I submit my new password')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('password', 'Password1')
    context.browser.fill('confirm_password', 'Password1')
    time.sleep(2)
    # print(User.objects.get(username=username).__dict__)
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I see a notification of password changed')
def step_impl(context):
    pass
    #Password successfully changed for mben03@gmail.com

@then(u'I shall login with the new password')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'Password1')
    time.sleep(2)
    print(User.objects.get(username=username).__dict__)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'
    context.browser.find_link_by_href('/logout/').click()

@when(u'I submit my un matching passwords')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('password', 'Password1')
    context.browser.fill('confirm_password', 'Password2')
    time.sleep(2)
    # print(User.objects.get(username=username).__dict__)
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I see a notification of passwords do not match')
def step_impl(context):
    pass

@then(u'I shall login with the old password')
def step_impl(context):
    context.browser.visit('http://localhost:4000/login/')
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'pass')
    time.sleep(2)
    print(User.objects.get(username=username).__dict__)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'
    context.browser.find_link_by_href('/logout/').click()