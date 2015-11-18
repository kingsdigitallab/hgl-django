# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.BooleanField(default=True)),
                ('family_or_institution_name', models.CharField(max_length=50, null=True, blank=True)),
                ('given_names', models.CharField(max_length=50, null=True, blank=True)),
                ('date', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VariantAttestation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_reference', models.CharField(max_length=30, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('link', models.CharField(max_length=500, null=True, blank=True)),
                ('author', models.ForeignKey(blank=True, to='geo.Author', null=True)),
                ('name_variant', models.ForeignKey(to='geo.Locus_Variant')),
                ('title', models.ForeignKey(blank=True, to='geo.Publication', null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='heritage',
            options={'verbose_name': 'Provenance'},
        ),
        migrations.AddField(
            model_name='coordinate',
            name='third_party_uri',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(blank=True, to='geo.PublicationType', null=True),
        ),
    ]
