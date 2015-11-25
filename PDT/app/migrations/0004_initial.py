# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='developerid',
        ),
        migrations.AddField(
            model_name='iteration',
            name='sloc',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='developers',
            field=models.ManyToManyField(to='app.Developer'),
        ),
        migrations.AddField(
            model_name='project',
            name='totalsloc',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='totaltime',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
