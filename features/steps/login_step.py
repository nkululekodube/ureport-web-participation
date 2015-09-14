from behave import *
import time
import uuid as uuid
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter

email = 'mbakoola@gmail.com'
username = 'user999999900'
password = 'password'
uid = uuid.uuid4()

@given(u'I am a registered user')
def step_impl(context):
    time.sleep(1)
    pass

@when(u'I visit the login page')
def step_impl(context):
    Ureporter.objects.create(uuid=uid, user=User.objects.create_user(username=username, email=email, password=password))
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
    # print(Ureporter.objects.all()[0].__dict__)
    # print(context.base_url, context.browser.url)

@then(u'I shall login')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('email', 'mbakoola@gmail.com')
    context.browser.fill('password', password)
    time.sleep(1)
    print(User.objects.get(username=username).__dict__)
    context.browser.find_by_css('.wp-send.btn').click()


@then(u'I see the link to logout')
def step_impl(context):
    time.sleep(2)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'

@then(u'I should be able logout')
def step_impl(context):
    time.sleep(1)
    context.browser.find_link_by_href('/logout/').click()
