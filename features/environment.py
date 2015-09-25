import time
import uuid as uuid
from splinter.browser import Browser
from django.contrib.auth.models import User
from webparticipation.apps.ureporter.models import Ureporter
from webparticipation.apps.ureport_auth.models import PasswordReset

def before_all(context):
    context.browser = Browser('chrome')
    time.sleep(5)

def before_scenario(context, scenario):

    email = 'ureport@webpro.com'
    username = 'user999999999'
    password = 'password'
    email1 = 'webpro@gmail.com'
    username1 = 'user999999991'
    uid = uuid.uuid4()
    uid1 = uuid.uuid4()

    Ureporter.objects.create(uuid=uid,
                             user=User.objects.create_user(username=username, email=email, password=password))
    Ureporter.objects.create(uuid=uid1,
                             user=User.objects.create_user(username=username1, email=email1, password=password))

def after_scenario(context, scenario):
    User.objects.all().delete()
    Ureporter.objects.all().delete()
    PasswordReset.objects.all().delete()

def after_all(context):
    context.browser.quit()
    context.browser = None
    context.server = None