import os
from splinter.browser import Browser
import subprocess
import time
import uuid as uuid
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.ureport_auth.models import PasswordReset

def before_all(context):
    context.base_url = "http://localhost:4000/"
    context.server = subprocess.Popen('python manage.py runserver 4000', shell=True)
    context.browser = Browser('chrome')
    time.sleep(5)

def before_scenario(context, scenario):
    email = 'mben03@gmail.com'
    username = 'user999999999'
    password = 'password'
    email1 = 'user@gmail.com'
    username1 = 'user999999991'
    uid = uuid.uuid4()
    uid1 = uuid.uuid4()

    Ureporter.objects.create(uuid=uid,
                             user=User.objects.create_user(username=username, email=email, password=password))

    Ureporter.objects.create(uuid=uid1,
                             user=User.objects.create_user(username=username1, email=email1, password=password))


def after_scenario(context, scenario):
    User.objects.all().delete()
    PasswordReset.objects.all().delete()


def after_all(context):
    context.browser.quit()
    context.browser = None
    subprocess.Popen('lsof -t -i:4000 | xargs kill', shell=True)
    context.server = None