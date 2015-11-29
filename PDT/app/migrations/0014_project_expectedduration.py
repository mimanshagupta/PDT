# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expectedduration',
            field=models.IntegerField(default=0),
        ),
    ]
