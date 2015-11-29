# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20151129_0644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='founditer',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='lastend',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='laststart',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='timecost',
        ),
        migrations.AddField(
            model_name='defect',
            name='defect_type',
            field=models.CharField(null=True, max_length=200, verbose_name='Defect Type', choices=[('requirement', 'inception'), ('design', 'elaboration'), ('implementation', 'construction'), ('badfix', 'badfix')]),
        ),
        migrations.AddField(
            model_name='defect',
            name='resolved_by',
            field=models.OneToOneField(null=True, to='app.Developer'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='defect_lastend',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='iteration',
            name='defect_laststart',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='iteration',
            name='defect_timecost',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
