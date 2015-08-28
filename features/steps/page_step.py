from behave import *
import page_actions
import time

@given(u'I am a visitor to webpro')
def step_impl(context):
    pass

@when(u'I browse to webpro')
def step_impl(context):
    context.browser.visit('http://localhost:4000/')
    time.sleep(1)

@then(u'I shall see a link to register')
def step_impl(context):
    assert context.browser.find_link_by_href("/register/"), 'Become_a_UReporter_Today link not found!'

@then(u'I shall also see a link to login')
def step_impl(context):
    assert context.browser.find_link_by_href("/login/?next=/"), 'Login link not found!'