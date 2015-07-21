from __future__ import with_statement
from fabric.api import *

env.key_filename = ['webpro-key.pem']
env.hosts = ["ubuntu@ec2-52-18-73-186.eu-west-1.compute.amazonaws.com"]


def deploy():
    with cd('www/ureport-web-participation'):
        run("git reset --hard")
        run("git pull")

    with cd("www/ureport-web-participation"):
        run("source env/bin/activate && pip install -r reqs/dev.txt")

    with cd('www/ureport-web-participation/'):
        sudo("supervisorctl restart uwsgi-builder")
        sudo("supervisorctl restart builder_celery")
