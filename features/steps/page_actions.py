import os
import time
from django.utils import timezone

def go_to_web_pro(context):
    context.browser.visit(context.base_url)
    time.sleep(1)

def hide_tool_bar(context):
    time.sleep(1)
    context.browser.find_by_id('djHideToolBarButton').click()

def go_to_login(context):
    time.sleep(1)
    context.browser.visit(context.base_url + 'login/')

def get_become_reporter_btn(context):
    time.sleep(1)
    return context.browser.find_link_by_href('/register/').first()

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

