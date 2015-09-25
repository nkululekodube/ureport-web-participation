from behave import *
import uuid as uuid
from page_actions import *
from page_objects import *

username = 'user999999999'
uid = uuid.uuid4()
email_address = 'ureport@webpro.com'
password = 'password'

@given(u'I am a registered user')
def step_impl(context):
    time.sleep(1)
    pass

@when(u'I visit the login page')
def step_impl(context):
    go_to_login_page(context)
    time.sleep(1)
@then(u'I shall login')
def step_impl(context):
    login_to_web_pro(context, email_address, password)

@then(u'I see the link to logout')
def step_impl(context):
    time.sleep(2)
    assert logout_link(context.browser), 'Logout link not found'

@then(u'I should be able logout')
def step_impl(context):
    log_out_of_web_pro(context)
    time.sleep(1)
    assert login_link(context.browser), 'Login link not found'
