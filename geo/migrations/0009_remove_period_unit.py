# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0008_auto_20151123_1424"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="period",
            name="unit",
        ),
    ]
