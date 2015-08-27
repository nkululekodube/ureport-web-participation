from behave import *
import time
import os
import page_actions
from django.contrib.auth.models import User

email = 'mben03@gmail.com'
username = 'user999999999'
password = 'pass'

@given(u'I am a regsterd user')
def step_impl(context):
    User.objects.create(username=username, email=email, password=password)
    context.browser.visit("http://localhost:8200/login/")
    time.sleep(1)


@when(u'I log in to webpro')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'pass')
    time.sleep(1)
    context.browser.find_by_css('.wp-send.btn').click()

@then(u'I see the link to logout')
def step_impl(context):
    time.sleep(1)
    assert context.browser.find_link_by_href('/logout/'), 'Link not found'

@then(u'I logout')
def step_impl(context):
    time.sleep(1)
    context.browser.find_link_by_href('/logout/').click()
