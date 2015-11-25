# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='description',
            field=models.CharField(verbose_name='Defect Description', max_length=200),
        ),
        migrations.AlterField(
            model_name='defect',
            name='founditer',
            field=models.PositiveIntegerField(verbose_name='Iteration Found', null=True),
        ),
        migrations.AlterField(
            model_name='defect',
            name='removediter',
            field=models.PositiveIntegerField(verbose_name='Iteration Removed', null=True),
        ),
    ]
