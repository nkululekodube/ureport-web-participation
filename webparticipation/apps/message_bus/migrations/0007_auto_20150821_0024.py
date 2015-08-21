# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_bus', '0006_auto_20150821_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagebus',
            name='msg_from',
            field=models.CharField(default=None, max_length=64),
        ),
    ]
