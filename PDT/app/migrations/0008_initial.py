# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='projectid',
            field=models.PositiveIntegerField(null=True, verbose_name='Project ID'),
        ),
    ]
