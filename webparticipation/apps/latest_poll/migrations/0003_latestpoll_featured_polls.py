# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_poll', '0002_auto_20150820_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='latestpoll',
            name='featured_polls',
            field=models.CommaSeparatedIntegerField(default=b'', max_length=4096),
        ),
    ]
