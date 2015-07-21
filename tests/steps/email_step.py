import os
from behave import *
# from splinter import Browser
from splinter import driver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email = 'mben03@gmail.com';

@given(u'I am a new user')
def step_impl(context):
    pass


@when(u'I browse to u-report website')
def step_impl(context):
    context.browser.visit('http://localhost:8000/register')

@when(u'I fill in critical registration details')
def step_impl(context):
    # wait_page_load(context.browser.find_by_id('btnSend'))
    context.browser.fill('send', email)

@when(u'I click submit critical registration details')
def step_impl(context):
    send = context.browser.find_by_id('btnSend')
    send.click()
    time.sleep(0)

@then(u'I shall be a registered u-reporter.')
def step_impl(context):

    # attributes = context.browser.find_by_css("ul.messages")
    # for attribute in attributes:
    #     if attribute.find_by_tag('li').first.value == 'mben03@gmail.com':
    #         print ("Email registered")
    #     else:
    #         print ("Email not registered")

    assert context.browser.is_text_present(email), 'Email not registered..'


    if context.browser.is_text_present(email):
        print ("Email registered")
    else:
        print ("Email not registered")
# send |btnSend

