from behave import *
import page_actions
import time

@given(u'I am a visitor to webpro')
def step_impl(context):
    page_actions.go_to_web_pro(context)


@when(u'I browse to webpro')
def step_impl(context):
    pass

@then(u'I shall see a link to register')
def step_impl(context):
    assert context.browser.find_link_by_href("/register/"), 'Become_a_UReporter_Today link not found!'

@then(u'I shall also see a link to login')
def step_impl(context):
    assert context.browser.find_link_by_href("/login/?next=/"), 'Login link not found!'