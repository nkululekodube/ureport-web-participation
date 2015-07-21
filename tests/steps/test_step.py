# import pytest
from behave import *
import time

@given(u'I am beneth')
def step_impl(context):
    """Test using real browser."""
    pass

@when(u'I browse to google')
def step_impl(context):
     url = "http://www.google.com"
     context.browser.visit(url)

@when(u'the page is ready')
def step_impl(context):
    pass

@when(u'I type in something')
def step_impl(context):
    context.browser.fill('q', 'splinter - python acceptance testing for web applications')
    # Find and click the 'search' button

@when(u'I click search')
def step_impl(context):
    # context.browser.submit()
    searchBtn = context.browser.find_by_name('btnG')
    # Interact with elements
    searchBtn.click()


@then(u'I shall see results of something.')
def step_impl(context):
    assert context.browser.is_text_present('splinter.readthedocs.org'), 'splinter.readthedocs.org was not found... '
    # context.browser.find_link_by_partial_href('splinter.readthedocs.org').click()
    context.browser.click_link_by_partial_href('https://splinter.readthedocs.org')
    time.sleep(10)

