# Generated by Django 5.0.8 on 2024-09-09 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0009_remove_download_moderator_remove_download_teacher"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="science_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.sciencetypes",
                verbose_name="Fan turi",
            ),
        ),
    ]
