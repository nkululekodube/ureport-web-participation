from behave import *
import page_actions
import time
from django.contrib.auth.models import User


@when(u'I login to u-report')
def step_impl(context):
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.fill('password', 'password')
    time.sleep(1)
    context.browser.find_by_css('.wp-send.btn').click()
    pass

@when(u'I go to the profile page')
def step_impl(context):
    time.sleep(2)
    assert context.browser.find_link_by_text('Profile'), 'Logout link not found'
    time.sleep(1)
    context.browser.find_link_by_text('Profile').click()
    pass

@when(u'I deactivate my account')
def step_impl(context):
    time.sleep(1)
    context.browser.find_by_css('.btn.btn-deactivate').click()
    time.sleep(2)
    context.browser.find_by_css('.btn.btn-danger').click()
    time.sleep(3)

@then(u'I see a notification for account deactivated successfully')
def step_impl(context):
    time.sleep(2)
    assert context.browser.is_text_present("We're sorry to see you go."), 'sorry_to_see_you_go not found'

@then(u'I shall not be able to login')
def step_impl(context):
    context.browser.visit(context.base_url + '/login/')
    time.sleep(1)
    context.browser.fill('email', 'ureport@webpro.com')
    context.browser.fill('password', 'password')
    time.sleep(1)
    context.browser.find_by_css('.wp-send.btn').click()
    time.sleep(1)
    assert context.browser.is_text_present('There is no registered user with sign-in email ureport@webpro.com'), 'No registered user notification not found'
    pass