# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('height', models.DecimalField(max_digits=10, decimal_places=7)),
                ('feature', models.CharField(max_length=200, null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Geojson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geojson', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Heritage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('recorded_by', models.CharField(max_length=200, null=True, blank=True)),
                ('hardware', models.CharField(max_length=200, null=True, blank=True)),
                ('accuracy', models.CharField(max_length=10, null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inscription_id', models.CharField(unique=True, max_length=15)),
                ('title', models.CharField(max_length=256)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inscription_Locus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context', models.TextField(null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('inscription', models.ForeignKey(to='geo.Inscription')),
            ],
            options={
                'verbose_name': 'Inscription Location',
                'verbose_name_plural': 'Inscriptions Locations',
            },
        ),
        migrations.CreateModel(
            name='Inscription_Locus_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Inscription Location Type',
                'verbose_name_plural': 'Inscription Location Types',
            },
        ),
        migrations.CreateModel(
            name='Locus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('pleiades_uri', models.URLField(null=True, blank=True)),
                ('featuretype', models.IntegerField(default=0, choices=[(0, b'point'), (1, b'line'), (2, b'polygon')])),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Locus_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Location Type',
                'verbose_name_plural': 'Location Types',
            },
        ),
        migrations.CreateModel(
            name='Locus_Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('locus', models.ForeignKey(related_name='variants', to='geo.Locus')),
            ],
            options={
                'verbose_name': 'Variant Name',
                'verbose_name_plural': 'Variant Names',
            },
        ),
        migrations.CreateModel(
            name='Related_Locus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_from', models.DateTimeField(null=True, blank=True)),
                ('date_to', models.DateTimeField(null=True, blank=True)),
                ('obj', models.ForeignKey(related_name='object', to='geo.Locus')),
            ],
            options={
                'verbose_name': 'Related Location',
                'verbose_name_plural': 'Related Locations',
            },
        ),
        migrations.CreateModel(
            name='Related_Locus_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('reciprocal_name', models.CharField(max_length=255, null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Related Location Type',
                'verbose_name_plural': 'Related Location Types',
            },
        ),
        migrations.AddField(
            model_name='related_locus',
            name='related_locus_type',
            field=models.ForeignKey(to='geo.Related_Locus_Type'),
        ),
        migrations.AddField(
            model_name='related_locus',
            name='subject',
            field=models.ForeignKey(related_name='subject', to='geo.Locus'),
        ),
        migrations.AddField(
            model_name='locus',
            name='locus_type',
            field=models.ForeignKey(blank=True, to='geo.Locus_Type', null=True),
        ),
        migrations.AddField(
            model_name='locus',
            name='related_locus',
            field=models.ManyToManyField(to='geo.Locus', through='geo.Related_Locus'),
        ),
        migrations.AddField(
            model_name='inscription_locus',
            name='inscription_locus_type',
            field=models.ForeignKey(to='geo.Inscription_Locus_Type'),
        ),
        migrations.AddField(
            model_name='inscription_locus',
            name='locus',
            field=models.ForeignKey(to='geo.Locus'),
        ),
        migrations.AddField(
            model_name='inscription',
            name='locus',
            field=models.ManyToManyField(to='geo.Locus', null=True, through='geo.Inscription_Locus', blank=True),
        ),
        migrations.AddField(
            model_name='geojson',
            name='locus',
            field=models.ForeignKey(related_name='locus_geojson', to='geo.Locus'),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='heritage',
            field=models.ForeignKey(to='geo.Heritage'),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='locus',
            field=models.ForeignKey(related_name='locus_coordinate', to='geo.Locus'),
        ),
        migrations.AlterUniqueTogether(
            name='related_locus',
            unique_together=set([('subject', 'obj', 'related_locus_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='inscription_locus',
            unique_together=set([('inscription', 'locus', 'inscription_locus_type')]),
        ),
    ]
