# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0004_auto_20151117_1530"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="locus",
            name="featuretype_fk",
        ),
        migrations.AddField(
            model_name="locus",
            name="featuretype_fk",
            field=models.ManyToManyField(to="geo.FeatureTypes", null=True, blank=True),
        ),
    ]
