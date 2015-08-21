# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ureporter', '0003_ureporter_urn_tel'),
    ]

    operations = [
        migrations.AddField(
            model_name='ureporter',
            name='last_poll_taken',
            field=models.IntegerField(default=0),
        ),
    ]
