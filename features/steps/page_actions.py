import os
import time
from page_objects import *

def go_to_web_pro(context):
    context.browser.visit(context.base_url+ '/login/')
    time.sleep(1)

def hide_tool_bar(context):
    time.sleep(1)
    context.browser.find_by_id('djHideToolBarButton').click()

def go_to_login_page(context):
    time.sleep(1)
    return context.browser.visit(context.base_url + '/login/')

def go_to_profile_page(context):
    time.sleep(1)
    return context.browser.visit(context.base_url + '/profile/')

def go_to_shout_page(context):
    time.sleep(1)
    return context.browser.visit(context.base_url + '/shout/')

def go_to_register_page(context):
    time.sleep(1)
    return context.browser.visit(context.base_url + '/register/')

def login_to_web_pro(context, email, password):
    time.sleep(1)
    context.browser.visit(context.base_url + '/login/')
    context.browser.fill('email', email)
    context.browser.fill('password', password)
    time.sleep(1)
    send_submit_btn(context.browser).click()

def deactivate_profile(browser):
    time.sleep(1)
    browser.find_link_by_href('/profile/deactivate/').click()
    time.sleep(2)
    browser.find_by_css('.btn.btn-danger').click()
    time.sleep(3)


def send_a_message(browser, message):
    browser.fill('message', message)
    time.sleep(1)
    send_submit_btn(browser).click()
    time.sleep(1)

def log_out_of_web_pro(context):
    time.sleep(2)
    assert logout_link(context.browser), 'Logout link not found'
    logout_link(context.browser).click()
    time.sleep(1)
    go_to_login_page(context)
    time.sleep(1)

def get_become_reporter_btn(context):
    time.sleep(1)
    return register_link.first(context.browser)


def reset_password(browser, password, confirm_password):
    time.sleep(1)
    browser.fill('password', password)
    browser.fill('confirm_password', confirm_password)
    time.sleep(2)
    browser.find_by_css('.wp-send.btn').click()

def send_forgot_password_email(browser, email):
    time.sleep(2)
    browser.fill('email', email)
    browser.find_by_css('.wp-send.btn').click()
    time.sleep(1)
