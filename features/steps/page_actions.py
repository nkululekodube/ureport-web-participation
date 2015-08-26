import os

def go_to_webpro(context):
    context.get_url()
    # browser.visit(os.environ.get('WEBPARTICIPATION_ROOT') + '/')
    context.browser.find_by_id('djHideToolBarButton').click()

def go_to_login(context):
    context.get_url('/login/')
    # browser.visit(os.environ.get('WEBPARTICIPATION_ROOT') + '/login/')
    context.browser.find_by_id('djHideToolBarButton').click()

def get_become_reporter_btn(context):
    return context.browser.find_by_css('.btn.btn-lg.btn-primary').first.click()
# href="/register/"

def get_login_btn(context):
    return context.browser.find_by_css('.btn.btn-lg.btn-primary').first.click()

# href="/login/?next=/"