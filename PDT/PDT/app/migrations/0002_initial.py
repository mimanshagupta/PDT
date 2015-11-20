# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteration',
            name='lastend',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iteration',
            name='timecost',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
