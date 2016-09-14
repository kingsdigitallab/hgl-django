# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0010_auto_20151123_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locus_variant',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
