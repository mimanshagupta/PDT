# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='totalsloc',
        ),
        migrations.RemoveField(
            model_name='project',
            name='totaltime',
        ),
    ]
