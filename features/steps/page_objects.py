
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

def email_input_field(browser):
    return browser.find_by_name('email')

def no_user_notification_present(browser, email):
    return browser.is_text_present('There is no registered user with sign-in email ' + email)

def password_unmatched_notification_present(browser):
    return browser.is_text_present('Password do not match')

def sorry_to_go_notification_present(browser):
    return browser.is_text_present("We're sorry to see you go.")

def password_changed_notification_present(browser, email):
    return browser.is_text_present('Password successfully changed for ' + email)

def change_password_failed_notification_present(browser, email):
    return browser.is_text_present('Password successfully changed for ' + email)

def sent_email_notification_present(browser, email):
    return browser.is_text_present('We have sent an email to ' + email)
