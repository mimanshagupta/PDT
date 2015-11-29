# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20151129_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='defect',
            name='removedphase',
            field=models.CharField(null=True, max_length=200, choices=[('inception', 'inception'), ('elaboration', 'elaboration'), ('construction', 'construction'), ('transition', 'transition')], verbose_name='Phase Removed'),
        ),
        migrations.AlterField(
            model_name='defect',
            name='defect_type',
            field=models.CharField(null=True, max_length=200, choices=[('requirement', 'requirement'), ('design', 'design'), ('implementation', 'implementation'), ('badfix', 'badfix')], verbose_name='Defect Type'),
        ),
        migrations.AlterField(
            model_name='defect',
            name='description',
            field=models.CharField(null=True, max_length=200, verbose_name='Defect Description'),
        ),
    ]
