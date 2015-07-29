# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ureporter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ureporter',
            name='email',
        ),
        migrations.RemoveField(
            model_name='ureporter',
            name='password',
        ),
        migrations.RemoveField(
            model_name='ureporter',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='ureporter',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
