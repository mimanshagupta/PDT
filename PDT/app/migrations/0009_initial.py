# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='sloc',
            field=models.IntegerField(default=0),
        ),
    ]
