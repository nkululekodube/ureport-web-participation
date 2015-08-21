# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_bus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagebus',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='messagebus',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='messagebus',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='messagebus',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='messagebus',
            name='modified_on',
        ),
    ]
