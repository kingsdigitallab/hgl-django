# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0006_auto_20151119_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinate',
            name='height',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=7, blank=True),
        ),
    ]
