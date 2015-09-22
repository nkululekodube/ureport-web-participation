from behave import *
import time
import uuid as uuid
from django.contrib.auth.models import User

username = 'user999999999'
uid = uuid.uuid4()

@given(u'I am a registered user')
def step_impl(context):
    time.sleep(1)
    pass

@when(u'I visit the login page')
def step_impl(context):
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
@then(u'I shall login')
def step_impl(context):
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.fill('password', 'password')
    time.sleep(1)
    context.browser.find_by_css('.wp-send.btn').click()


@then(u'I see the link to logout')
def step_impl(context):
    time.sleep(2)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'

@then(u'I should be able logout')
def step_impl(context):
    time.sleep(1)
    context.browser.find_link_by_href('/logout/').click()
    time.sleep(1)
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
