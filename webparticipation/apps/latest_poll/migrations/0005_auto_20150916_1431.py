# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_poll', '0004_auto_20150916_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestpoll',
            name='featured_polls',
            field=models.CommaSeparatedIntegerField(default=b'0', max_length=4096),
        ),
    ]
