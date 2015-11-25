# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='defect',
            old_name='injectediter',
            new_name='founditer',
        ),
        migrations.AddField(
            model_name='defect',
            name='lastend',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defect',
            name='laststart',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defect',
            name='timecost',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
