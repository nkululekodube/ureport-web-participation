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
    user = User.objects.create(username=username, email=email, password=password)
    url=context.browser.visit(os.environ.get('WEBPARTICIPATION_ROOT') + '/')
    context.browser.find_by_id('djHideToolBarButton').click()
    print (url)
    # Ureporter.objects.create(user=user)
    # u.set_password(password)

@when(u'I log in to webpro')
def step_impl(context):
    # context.get_url('/login/')
    time.sleep(1)
    context.browser.fill('email', 'mben03@gmail.com')
    context.browser.fill('password', 'pass')
    time.sleep(1)
    context.browser.submit()

@then(u'I see the home page')
def step_impl(context):
    br = context.browser
    assert context.browser.is_text_present("Profile"), 'Profile link not found!'

@then(u'I also see link to logout')
def step_impl(context):
    assert context.browser.is_text_present("Logout"), 'Logout link not found!'


