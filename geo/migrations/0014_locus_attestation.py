# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0013_locus_variant_attestation'),
    ]

    operations = [
        migrations.AddField(
            model_name='locus',
            name='attestation',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
