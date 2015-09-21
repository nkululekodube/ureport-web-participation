# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webparticipation.apps.ureporter.models


class Migration(migrations.Migration):

    dependencies = [
        ('ureporter', '0005_ureporter_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ureporter',
            name='unsubscribe_token',
            field=models.CharField(default=webparticipation.apps.ureporter.models.generate_unsubscribe_token, max_length=32),
        ),
    ]
