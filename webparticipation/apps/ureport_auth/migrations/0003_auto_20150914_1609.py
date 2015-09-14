# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ureport_auth', '0002_passwordreset_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='user',
            field=models.ForeignKey(default=b'auth.User', to=settings.AUTH_USER_MODEL),
        ),
    ]
