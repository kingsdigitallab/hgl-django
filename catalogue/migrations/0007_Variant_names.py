# Generated by Django 3.2.21 on 2023-09-19 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_person_referencetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='alternativename',
            name='DateFrom',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alternativename',
            name='defaultName',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alternativename',
            name='referenceType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.referencetype'),
        ),
    ]
