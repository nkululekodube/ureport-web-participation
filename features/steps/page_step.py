from behave import *
from page_actions import *
from page_objects import *

@given(u'I am a visitor to web-pro')
def step_impl(context):
    pass

@when(u'I browse to web-pro')
def step_impl(context):
    go_to_web_pro(context)
    time.sleep(1)

@then(u'I shall see a link to login')
def step_impl(context):
    time.sleep(1)
    assert login_link(context.browser), 'Login link not found!'
