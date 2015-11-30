# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20151130_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='defaultyield',
            field=models.PositiveIntegerField(default=80),
        ),
        migrations.AlterField(
            model_name='project',
            name='expectedduration',
            field=models.IntegerField(default=1),
        ),
    ]
