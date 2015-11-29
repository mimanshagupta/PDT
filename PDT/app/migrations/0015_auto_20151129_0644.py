# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_project_expectedduration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('phaseid', models.AutoField(serialize=False, primary_key=True)),
                ('projectid', models.PositiveIntegerField(null=True, verbose_name='Project ID')),
                ('phase_name', models.CharField(choices=[('inception', 'inception'), ('elaboration', 'elaboration'), ('construction', 'construction'), ('transition', 'transition')], max_length=200, verbose_name='Phase Name')),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='phase',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
