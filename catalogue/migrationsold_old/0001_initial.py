# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BasicArchiveModel",
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
                ("unittitle", models.CharField(max_length=100)),
                ("unitstart_date", models.IntegerField()),
                ("unitend_date", models.IntegerField()),
                ("scopecontent", models.TextField(null=True, blank=True)),
                ("arrangement", models.TextField(null=True, blank=True)),
                ("custodhist", models.TextField(null=True, blank=True)),
                ("relatedmaterial", models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Language",
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
                ("desc", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Level",
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
                ("desc", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Note",
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
                ("text", models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="NoteAudience",
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
                ("desc", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="NoteType",
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
                ("desc", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="PhysDesc",
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
                ("desc", models.TextField(null=True, blank=True)),
                (
                    "item",
                    models.ForeignKey(
                        blank=True, to="catalogue.BasicArchiveModel", null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PhysDescType",
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
                ("desc", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Repository",
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
                ("desc", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="UnitId",
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
                ("desc", models.TextField(null=True, blank=True)),
                (
                    "item",
                    models.ForeignKey(
                        blank=True, to="catalogue.BasicArchiveModel", null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UnitIdType",
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
                ("desc", models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name="unitid",
            name="type",
            field=models.ForeignKey(to="catalogue.UnitIdType"),
        ),
        migrations.AddField(
            model_name="physdesc",
            name="type",
            field=models.ForeignKey(to="catalogue.PhysDescType"),
        ),
        migrations.AddField(
            model_name="note",
            name="audience",
            field=models.ForeignKey(to="catalogue.NoteAudience"),
        ),
        migrations.AddField(
            model_name="note",
            name="item",
            field=models.ForeignKey(
                blank=True, to="catalogue.BasicArchiveModel", null=True
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="type",
            field=models.ForeignKey(to="catalogue.NoteType"),
        ),
        migrations.AddField(
            model_name="basicarchivemodel",
            name="language",
            field=models.ForeignKey(blank=True, to="catalogue.Language", null=True),
        ),
        migrations.AddField(
            model_name="basicarchivemodel",
            name="level",
            field=models.ForeignKey(to="catalogue.Level"),
        ),
        migrations.AddField(
            model_name="basicarchivemodel",
            name="parent",
            field=models.ForeignKey(
                related_name="children",
                blank=True,
                to="catalogue.BasicArchiveModel",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="basicarchivemodel",
            name="repository",
            field=models.ForeignKey(to="catalogue.Repository"),
        ),
    ]
