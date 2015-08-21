# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_bus', '0004_auto_20150821_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagebus',
            name='msg_to',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
