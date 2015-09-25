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
    br = context.browser
    time.sleep(1)
    context.browser.visit(context.base_url + '/login/')
    context.browser.fill('email', email)
    context.browser.fill('password', password)
    time.sleep(1)
    send_submit_btn(br).click()

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
    logout_link(context.browser).click()
    time.sleep(1)
    go_to_login_page(context)
    time.sleep(1)

def get_become_reporter_btn(context):
    time.sleep(1)
    return register_link.first(context.browser)

def get_login_btn(context):
    time.sleep(1)
    return context.browser.find_by_css('/login/?next=/').first()

def take_screen_shot(context):
    time.sleep(1)
    filename = context.browser.screenshot(name='screen-shot-' % timezone.now().__str__(), suffix='jpeg')
    # context.assertTrue(tempfile.gettempdir() in filename)

def take_screenshot(driver):
    name = 'screen-shot-' % timezone.now().__str__()
    save_location="../../webparticipation/screenshots"
    path = os.path.abspath(save_location)
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = '%s/%s' % (path, name)
    driver.get_screenshot_as_file(full_path)
    return full_path

