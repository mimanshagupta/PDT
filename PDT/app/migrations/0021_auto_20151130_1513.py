# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_defect_projectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='defaultyield',
            field=models.IntegerField(default=80),
        ),
        migrations.AlterField(
            model_name='project',
            name='phase',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)]),
        ),
    ]
