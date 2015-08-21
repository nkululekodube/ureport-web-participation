# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_bus', '0007_auto_20150821_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagebus',
            name='msg_text',
            field=models.CharField(default=None, max_length=160),
        ),
    ]
