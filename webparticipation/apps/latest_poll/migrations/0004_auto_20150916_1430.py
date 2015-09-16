# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('latest_poll', '0003_latestpoll_featured_polls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestpoll',
            name='featured_polls',
            field=models.CommaSeparatedIntegerField(default=0, max_length=4096),
        ),
    ]
