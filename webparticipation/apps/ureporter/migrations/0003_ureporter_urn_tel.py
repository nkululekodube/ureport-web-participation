# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ureporter', '0002_auto_20150729_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='ureporter',
            name='urn_tel',
            field=models.CharField(default='user111111111', max_length=13),
            preserve_default=False,
        ),
    ]
