# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0012_auto_20160106_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='locus_variant',
            name='attestation',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
