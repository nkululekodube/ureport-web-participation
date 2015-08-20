# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestpoll',
            name='poll_id',
            field=models.IntegerField(null=True),
        ),
    ]
