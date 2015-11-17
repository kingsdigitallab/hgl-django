# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_auto_20151117_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='related_locus',
            name='obj',
            field=models.ForeignKey(related_name='parent', verbose_name=b'Parent', to='geo.Locus'),
        ),
        migrations.AlterField(
            model_name='related_locus',
            name='related_locus_type',
            field=models.ForeignKey(verbose_name=b'Relationship', to='geo.Related_Locus_Type'),
        ),
        migrations.AlterField(
            model_name='related_locus',
            name='subject',
            field=models.ForeignKey(related_name='child', verbose_name=b'Child', to='geo.Locus'),
        ),
        migrations.AddField(
            model_name='locus',
            name='featuretype_fk',
            field=models.ForeignKey(blank=True, to='geo.FeatureTypes', null=True),
        ),
    ]
