from splinter.browser import Browser
import subprocess
import time


def before_all(context):
    context.server = subprocess.Popen(['python', 'manage.py', 'runserver', '8200'])
    print (context.server)
    context.browser = Browser('chrome')
    time.sleep(5)


def after_all(context):
    context.browser.quit()
    context.browser = None
    subprocess.Popen('lsof -t -i:8200 | xargs kill', shell=True)
    context.server = None
    print (context.server)
