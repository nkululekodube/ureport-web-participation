import os
import time

def go_to_web_pro(context):
    context.browser.visit('http://localhost:4000/')
    time.sleep(1)

def hide_tool_bar(context):
    time.sleep(1)
    context.browser.find_by_id('djHideToolBarButton').click()


def go_to_login(context):
    time.sleep(1)
    context.browser.visit('http://localhost:4000/login/')

def get_become_reporter_btn(context):
    time.sleep(1)
    return context.browser.find_link_by_href('/register/').first()

def get_login_btn(context):
    time.sleep(1)
    return context.browser.find_by_css('/login/?next=/').first()