from behave import *
import time


email = 'mben03@gmail.com'
wrong_code = '3457823232'
wrong_email = 'mben03&gmail.com'


def go_to_u_report(browser):
    browser.visit('http://localhost:8200/register')
    browser.find_by_id('djHideToolBarButton').click()


@given(u'I am a new user  with a wrong email format')
def step_impl(context):
    go_to_u_report(context.browser)


@when(u'I browse to u-report')
def step_impl(context):
    pass


@when(u'I enter a wrong format for an email address')
def step_impl(context):
    time.sleep(1)
    context.browser.fill('send', wrong_email)


@when(u'I click submit')
def step_impl(context):
    context.browser.find_by_css('.wp-send.btn').first.click()
    time.sleep(1)


@then(u'I should see a message "that does not seem to be a valid email address."')
def step_impl(context):
    time.sleep(1)
    assert context.browser.is_text_present("that does not seem to be a valid email address."), 'Invalid email'


@given(u'I am a new user with a correct email format')
def step_impl(context):
    pass


@when(u'I fill in my email address')
def step_impl(context):
    context.browser.fill('send', email)
    time.sleep(1)


@then(u'I shall see "my email" and a notification "Thanks! Just to confirm that you are actually you".')
def step_impl(context):
    assert context.browser.is_text_present(email), 'Email not registered..'
    time.sleep(1)


@given(u'I am a new user who has submitted their email address')
def step_impl(context):
    pass


@when(u'I misspell the verification code')
def step_impl(context):
    context.browser.fill('send', wrong_code)


@then(u'Then I should see a message "I\'m sorry, that\'s an invalid code."')
def step_impl(context):
    time.sleep(1)
    assert context.browser.is_text_present("I'm sorry, that's an invalid code."), 'Invalid code.1'


@given(u'I am already registered')
def step_impl(context):
    pass


@then(u'I shall see a notification "Email already registered".')
def step_impl(context):
    # assert context.browser.is_text_present('Email already registered'), 'Sorry, email already registered..'
    pass
