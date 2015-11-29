# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_iteration_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='defect',
            name='injectediter',
            field=models.PositiveIntegerField(verbose_name='Iteration Injected', null=True),
        ),
        migrations.AddField(
            model_name='defect',
            name='injectedphase',
            field=models.CharField(max_length=200, verbose_name='Phase Injected', null=True, choices=[('inception', 'inception'), ('elaboration', 'elaboration'), ('construction', 'construction'), ('transition', 'transition')]),
        ),
    ]
