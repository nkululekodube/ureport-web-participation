# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import webparticipation.apps.ureport_user.models


class Migration(migrations.Migration):

    dependencies = [
        ('ureport_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ureportuser',
            name='active',
        ),
        migrations.AlterField(
            model_name='ureportuser',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ureportuser',
            name='token',
            field=models.IntegerField(default=webparticipation.apps.ureport_user.models.generate_token),
        ),
    ]
