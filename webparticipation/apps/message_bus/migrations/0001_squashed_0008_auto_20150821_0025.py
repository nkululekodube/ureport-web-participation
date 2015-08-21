# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'message_bus', '0001_initial'), (b'message_bus', '0002_auto_20150820_2350'), (b'message_bus', '0003_auto_20150821_0009'), (b'message_bus', '0004_auto_20150821_0012'), (b'message_bus', '0005_auto_20150821_0020'), (b'message_bus', '0006_auto_20150821_0023'), (b'message_bus', '0007_auto_20150821_0024'), (b'message_bus', '0008_auto_20150821_0025')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageBus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg_id', models.PositiveIntegerField()),
                ('msg_channel', models.PositiveIntegerField()),
                ('msg_to', models.CharField(default=None, max_length=13)),
                ('msg_from', models.CharField(default=None, max_length=64)),
                ('msg_text', models.CharField(default=None, max_length=160)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
