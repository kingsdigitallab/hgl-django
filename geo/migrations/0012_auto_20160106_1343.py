# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0011_auto_20151123_1519"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="language",
            options={"ordering": ("en_name",)},
        ),
        migrations.AlterField(
            model_name="locus",
            name="featuretype",
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name=b"Geometry type",
                choices=[(0, b"point"), (1, b"line"), (2, b"polygon")],
            ),
        ),
    ]
