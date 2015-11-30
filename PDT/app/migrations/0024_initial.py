# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='defect',
            name='byname',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
