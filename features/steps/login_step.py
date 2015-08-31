from behave import *
import time
from django.contrib.auth.models import User

email = 'mben03@gmail.com'
username = 'user999999999'
password = 'pass'

email1 = 'user@gmail.com'
username1 = 'user999999991'
password = 'pass'

@given(u'I am a registered user')
def step_impl(context):
    User.objects.create(username=username, email=email, password=password)
    User.objects.create(username=username1, email=email1, password=password)
    time.sleep(2)


@when(u'I visit the login page')
def step_impl(context):
    context.browser.visit('http://localhost:4000/login/')
    time.sleep(1)

@then(u'I shall login')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'pass')
    time.sleep(2)
    print(User.objects.get(username=username).__dict__)
    context.browser.find_by_css('.wp-send.btn').click()


@then(u'I see the link to logout')
def step_impl(context):
    time.sleep(5)
    assert context.browser.find_link_by_href('/logout/'), 'Logout link not found'

@then(u'I should be able logout')
def step_impl(context):
    time.sleep(1)
    context.browser.find_link_by_href('/logout/').click()
