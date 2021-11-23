# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="basicarchivemodel",
            name="bioghist",
            field=models.TextField(null=True, blank=True),
        ),
    ]
