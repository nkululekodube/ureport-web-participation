import os
from splinter.browser import Browser
import subprocess
import time
# from webpaticipation.main.tests.factories import UserFactory, RandomContentFactory

def before_all(context):
    context.base_url = os.environ.get('WEBPARTICIPATION_ROOT')
    context.server = subprocess.Popen("export DJANGO_SETTINGS_MODULE='webparticipation.settings.testing'", shell=True)
    # context.server = subprocess.Popen("export DATABASE_NAME = 'webparticipation_test'", shell=True)

    # context.server = subprocess.Popen('python manage.py migrate  --settings=webparticipation.settings.testing', shell=True)
    # context.server = subprocess.Popen('python manage.py runserver 8200  --settings=webparticipation.settings.testing', shell=True)
    context.server = subprocess.Popen('python manage.py runserver 8200', shell=True)
    context.browser = Browser('chrome')
    time.sleep(5)

# def before_scenario(context, scenario):
#     UserFactory(username='user1')
#     UserFactory(username='user2')
#     RandomContentFactory()


def after_all(context):
    context.browser.quit()
    context.browser = None
    subprocess.Popen('lsof -t -i:8200 | xargs kill', shell=True)
    context.server = None
