from behave import *
import page_actions
import time

@given(u'I am a visitor to web-pro')
def step_impl(context):
    pass

@when(u'I browse to web-pro')
def step_impl(context):
    context.browser.visit(context.base_url)
    time.sleep(1)

@then(u'I shall see a link to register')
def step_impl(context):
    time.sleep(1)
    assert context.browser.find_link_by_href("/register/"), 'Become_a_UReporter_Today link not found!'

@then(u'I shall see a link to login')
def step_impl(context):
    time.sleep(1)
    assert context.browser.find_link_by_href("/login/"), 'Login link not found!'