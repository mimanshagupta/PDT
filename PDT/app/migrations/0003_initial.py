# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='timecost',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
