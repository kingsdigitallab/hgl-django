# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0016_auto_20160331_1522"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeatureCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("description", models.CharField(max_length=50)),
            ],
            options={
                "ordering": ("description",),
                "verbose_name_plural": "Feature categories",
            },
        ),
        migrations.AlterModelOptions(
            name="authority",
            options={"verbose_name_plural": "Authorities"},
        ),
        migrations.AlterModelOptions(
            name="featuretypes",
            options={
                "ordering": ("description",),
                "verbose_name_plural": "Feature types",
            },
        ),
        migrations.AlterModelOptions(
            name="locus_variant",
            options={
                "ordering": ["name"],
                "verbose_name": "Variant Name",
                "verbose_name_plural": "Variant Names",
            },
        ),
        migrations.AlterModelOptions(
            name="related_locus",
            options={
                "ordering": ["subject", "obj"],
                "verbose_name": "Related Location",
                "verbose_name_plural": "Related Locations",
            },
        ),
        migrations.AlterModelOptions(
            name="related_locus_type",
            options={
                "ordering": ["name", "reciprocal_name"],
                "verbose_name": "Related Location Type",
                "verbose_name_plural": "Related Location Types",
            },
        ),
        migrations.AddField(
            model_name="featuretypes",
            name="category",
            field=models.ForeignKey(blank=True, to="geo.FeatureCategory", null=True),
        ),
    ]
