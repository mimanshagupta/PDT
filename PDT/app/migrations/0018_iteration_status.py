# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20151129_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteration',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
