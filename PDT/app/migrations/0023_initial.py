# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20151130_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='resolved_by',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
