import os
import time

def go_to_web_pro(context):
    context.browser.visit(os.environ.get('WEBPARTICIPATION_ROOT') + '/')
    time.sleep(1)

def hide_tool_bar(context):
    time.sleep(1)
    context.browser.find_by_id('djHideToolBarButton').click()


def go_to_login(context):
    context.browser.visit(os.environ.get('WEBPARTICIPATION_ROOT') + '/login/')

def get_become_reporter_btn(context):
    return context.browser.find_link_by_href('/register/').first()

def get_login_btn(context):
    return context.browser.find_by_css('/login/?next=/').first()
