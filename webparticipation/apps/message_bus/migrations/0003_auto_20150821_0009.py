# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_bus', '0002_auto_20150820_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagebus',
            name='msg_text',
            field=models.CharField(max_length=160, blank=True),
        ),
    ]
