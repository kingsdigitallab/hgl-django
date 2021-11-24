# Generated by Django 3.2.9 on 2021-11-24 15:09

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.BooleanField(default=True)),
                ('family_or_institution_name', models.CharField(blank=True, max_length=50, null=True)),
                ('given_names', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('base_uri', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Authorities',
            },
        ),
        migrations.CreateModel(
            name='FeatureCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Feature categories',
                'ordering': ('description',),
            },
        ),
        migrations.CreateModel(
            name='FeatureTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.featurecategory')),
            ],
            options={
                'verbose_name_plural': 'Feature types',
                'ordering': ('description',),
            },
        ),
        migrations.CreateModel(
            name='Heritage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('recorded_by', models.CharField(blank=True, max_length=200, null=True)),
                ('hardware', models.CharField(blank=True, max_length=200, null=True)),
                ('accuracy', models.CharField(blank=True, max_length=10, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Provenance',
            },
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inscription_id', models.CharField(max_length=15, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inscription_Locus_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Inscription Location Type',
                'verbose_name_plural': 'Inscription Location Types',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('en_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ('en_name',),
            },
        ),
        migrations.CreateModel(
            name='Locus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Descriptor')),
                ('attestation', models.CharField(blank=True, help_text='(for default name, descriptor)', max_length=500, null=True)),
                ('geonames_id', models.IntegerField(blank=True, help_text='Redundant field, see external URI below', null=True)),
                ('pleiades_uri', models.URLField(blank=True, help_text='Redundant field, see external URI below', null=True)),
                ('featuretype', models.IntegerField(blank=True, choices=[(0, 'point'), (1, 'line'), (2, 'polygon')], null=True, verbose_name='Geometry type')),
                ('note', models.TextField(blank=True, help_text='Use sparingly!', null=True, verbose_name='Notes')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('geojsion', models.TextField(blank=True, null=True)),
                ('geojson_provenance', models.TextField(blank=True, null=True)),
                ('featuretype_fk', models.ManyToManyField(blank=True, null=True, to='geo.FeatureTypes')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Locus_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('note', models.TextField(blank=True, null=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('note', models.TextField(blank=True, null=True)),
                ('attestation', models.CharField(blank=True, max_length=500, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.language')),
                ('locus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='geo.locus')),
                ('provenance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.heritage')),
            ],
            options={
                'verbose_name': 'Variant Name',
                'verbose_name_plural': 'Variant Names',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Related_Locus_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('reciprocal_name', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Related Location Type',
                'verbose_name_plural': 'Related Location Types',
                'ordering': ['name', 'reciprocal_name'],
            },
        ),
        migrations.CreateModel(
            name='VariantAttestation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_reference', models.CharField(blank=True, max_length=30, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.author')),
                ('name_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.locus_variant')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.publication')),
            ],
        ),
        migrations.CreateModel(
            name='Related_Locus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_from', models.DateTimeField(blank=True, null=True)),
                ('date_to', models.DateTimeField(blank=True, null=True)),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='geo.locus', verbose_name='Parent')),
                ('period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.period')),
                ('related_locus_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.related_locus_type', verbose_name='Relationship')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='geo.locus', verbose_name='Child')),
            ],
            options={
                'verbose_name': 'Related Location',
                'verbose_name_plural': 'Related Locations',
                'ordering': ['subject', 'obj'],
                'unique_together': {('subject', 'obj', 'related_locus_type')},
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.publicationtype'),
        ),
        migrations.AddField(
            model_name='locus',
            name='locus_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.locus_type'),
        ),
        migrations.AddField(
            model_name='locus',
            name='related_locus',
            field=models.ManyToManyField(through='geo.Related_Locus', to='geo.Locus'),
        ),
        migrations.CreateModel(
            name='Inscription_Locus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('inscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.inscription')),
                ('inscription_locus_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.inscription_locus_type')),
                ('locus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.locus')),
            ],
            options={
                'verbose_name': 'Inscription Location',
                'verbose_name_plural': 'Inscriptions Locations',
                'unique_together': {('inscription', 'locus', 'inscription_locus_type')},
            },
        ),
        migrations.AddField(
            model_name='inscription',
            name='locus',
            field=models.ManyToManyField(blank=True, null=True, through='geo.Inscription_Locus', to='geo.Locus'),
        ),
        migrations.CreateModel(
            name='Geojson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geojson', models.TextField(blank=True, null=True)),
                ('locus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locus_geojson', to='geo.locus')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalURI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.TextField()),
                ('authority', models.ForeignKey(blank=True, help_text='Redundant - use Provenance below', null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.authority')),
                ('locus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.locus')),
                ('provenance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.heritage')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('height', models.DecimalField(blank=True, decimal_places=3, max_digits=11, null=True)),
                ('third_party_uri', models.CharField(blank=True, max_length=500, null=True)),
                ('feature', models.CharField(blank=True, max_length=200, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('heritage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.heritage')),
                ('locus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locus_coordinate', to='geo.locus')),
            ],
        ),
    ]
