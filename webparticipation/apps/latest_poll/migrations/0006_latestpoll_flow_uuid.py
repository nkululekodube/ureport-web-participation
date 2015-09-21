# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_poll', '0005_auto_20150916_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='latestpoll',
            name='flow_uuid',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
