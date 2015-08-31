from behave import *
import time
import os
import page_actions
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter

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
    # usr = User.objects.create(username=username1, email=email1, password=password)
    # Ureporter.objects.create(user=usr)
    time.sleep(2)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(1)
    print(User.objects.get(email='mben03@gmail.com').__dict__)


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
