from __future__ import with_statement
from fabric.api import *

env.key_filename = ['wep-pro-key.pem']
env.hosts = ["ubuntu@ec2-52-18-73-186.eu-west-1.compute.amazonaws.com"]


def deploy():
    with cd('www/ureport-web-participation'):
        run("git reset --hard")
        run("git pull")

def activate_env():
    with cd("www/ureport-web-participation"):
         run("source env/bin/activate && pip install -r reqs/common.txt")

def migrate():
    with cd("www/ureport-web-participation"):
         run("python manage.py makemigrations")
         run("pyhton manage.py migrate")
        
def services_up():
    with cd('www/ureport-web-participation/'):
         sudo("supervisorctl restart uwsgi-builder")
         sudo("supervisorctl restart builder_celery")
