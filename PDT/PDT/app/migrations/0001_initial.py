# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('workerid', models.AutoField(primary_key=True, serialize=False, verbose_name='Developer ID')),
                ('name', models.CharField(max_length=50, verbose_name='Developer Name')),
            ],
        ),
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('iterid', models.AutoField(primary_key=True, serialize=False)),
                ('iternumber', models.PositiveIntegerField(verbose_name='Iteration no')),
                ('phrase', models.CharField(max_length=50, verbose_name='Phrase')),
                ('projectid', models.PositiveIntegerField(null=True)),
                ('laststart', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False, verbose_name='Project ID')),
                ('name', models.CharField(max_length=200, verbose_name='Project Name')),
                ('developerid', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectManager',
            fields=[
                ('mid', models.AutoField(primary_key=True, serialize=False, verbose_name='Manager ID')),
                ('name', models.CharField(max_length=50, verbose_name='Manager Name')),
            ],
        ),
    ]
