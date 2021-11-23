# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0007_auto_20151123_1234"),
    ]

    operations = [
        migrations.CreateModel(
            name="Period",
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
                ("unit", models.ForeignKey(to="geo.Locus")),
            ],
            options={
                "ordering": ["description"],
            },
        ),
        migrations.AddField(
            model_name="related_locus",
            name="period",
            field=models.ForeignKey(blank=True, to="geo.Period", null=True),
        ),
    ]
