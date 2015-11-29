# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20151130_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='defect',
            name='projectid',
            field=models.PositiveIntegerField(verbose_name='Project ID', null=True),
        ),
    ]
