# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0005_auto_20151117_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='featuretypes',
            options={'ordering': ('description',)},
        ),
        migrations.AddField(
            model_name='locus',
            name='geonames_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='locus',
            name='featuretype',
            field=models.IntegerField(verbose_name=b'Geometry type', choices=[(0, b'point'), (1, b'line'), (2, b'polygon')]),
        ),
        migrations.AlterField(
            model_name='locus',
            name='name',
            field=models.CharField(unique=True, max_length=200, verbose_name=b'Descriptor'),
        ),
        migrations.AlterField(
            model_name='locus',
            name='note',
            field=models.TextField(help_text=b'Use sparingly!', null=True, verbose_name=b'Notes', blank=True),
        ),
    ]
