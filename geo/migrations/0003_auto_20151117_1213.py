# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0002_auto_20151117_1148"),
    ]

    operations = [
        migrations.RenameField(
            model_name="publication",
            old_name="type",
            new_name="publication_type",
        ),
    ]
