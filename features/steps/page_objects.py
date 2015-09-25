
def hide_tool_bar(context):
    return context.browser.find_by_id('djHideToolBarButton')

def profile_link(browser):
    return browser.find_link_by_href('/profile/')

def register_link(browser):
    return browser.find_link_by_href('/register/')

def login_link(browser):
    return browser.find_link_by_href('/login/')

def logout_link(browser):
    return browser.find_link_by_href('/logout/')

def send_submit_btn(browser):
    return browser.find_by_css('.wp-send.btn')

def un_registered_user_notification(browser, email):
    return browser.is_text_present('There is no registered user with sign-in email ' + email)