# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ureporter', '0004_ureporter_last_poll_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='ureporter',
            name='subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
