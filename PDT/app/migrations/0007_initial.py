# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('defid', models.AutoField(primary_key=True, serialize=False)),
                ('injectediter', models.PositiveIntegerField(null=True)),
                ('removediter', models.PositiveIntegerField(null=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='totalsloc',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='totaltime',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
