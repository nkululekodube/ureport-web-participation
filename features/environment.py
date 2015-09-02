import os
from splinter.browser import Browser
import subprocess
import time

def before_all(context):
    context.base_url = "http://localhost:4000/"
    context.server = subprocess.Popen('python manage.py runserver 4000', shell=True)
    context.browser = Browser('chrome')
    time.sleep(5)

def after_all(context):
    context.browser.quit()
    context.browser = None
    subprocess.Popen('lsof -t -i:4000 | xargs kill', shell=True)
    context.server = None