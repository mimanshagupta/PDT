# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expectedsloc',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='iterations',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='phase',
            field=models.IntegerField(default=1),
        ),
    ]
