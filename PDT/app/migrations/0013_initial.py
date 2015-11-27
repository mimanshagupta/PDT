# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20151126_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='iternumber',
            field=models.PositiveIntegerField(verbose_name='Iteration no.'),
        ),
        migrations.AlterField(
            model_name='iteration',
            name='phrase',
            field=models.CharField(verbose_name='Phase (Please enter as "inception", "elaboration", "construction", "transition")', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='phase',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='totalsloc',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='totaltime',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
