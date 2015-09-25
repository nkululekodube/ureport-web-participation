from behave import *
import time
from page_actions import *
from page_objects import *

email = 'ureport@webpro.com'
password = 'password'

@when(u'I login to u-report')
def step_impl(context):
    login_to_web_pro(context, email, password)
    time.sleep(1)

@when(u'I go to the profile page')
def step_impl(context):
    time.sleep(2)
    go_to_profile_page(context)

@when(u'I deactivate my account')
def step_impl(context):
    deactivate_profile(context.browser)
    time.sleep(2)
    assert context.browser.is_text_present("We're sorry to see you go."), 'sorry_to_see_you_go not found'


@then(u'I shall not be able to login')
def step_impl(context):
    login_to_web_pro(context, email, password)
    time.sleep(1)
    assert un_registered_user_notification(context.browser, email), 'No registered user notification not found'
