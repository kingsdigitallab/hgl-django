# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0014_locus_attestation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalURI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='locus',
            name='attestation',
            field=models.CharField(help_text=b'(for default name, descriptor)', max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='externaluri',
            name='locus',
            field=models.ForeignKey(to='geo.Locus'),
        ),
    ]
