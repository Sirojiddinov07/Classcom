# Generated by Django 5.1 on 2024-08-18 11:12

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("classcom", "0027_media_file_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ClassType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("name_uz", models.CharField(max_length=255, null=True)),
                ("name_ru", models.CharField(max_length=255, null=True)),
                ("name_en", models.CharField(max_length=255, null=True)),
            ],
            options={
                "verbose_name": "ClassType",
                "verbose_name_plural": "ClassTypes",
            },
        ),
        migrations.AddField(
            model_name="schedule",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="schedule",
            name="weekday",
            field=models.CharField(
                blank=True,
                choices=[
                    ("monday", "Monday"),
                    ("tuesday", "Tuesday"),
                    ("wednesday", "Wednesday"),
                    ("thursday", "Thursday"),
                    ("friday", "Friday"),
                    ("saturday", "Saturday"),
                ],
                max_length=15,
                null=True,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="schedule",
            unique_together={("date", "start_time", "end_time", "user")},
        ),
        migrations.AddField(
            model_name="classes",
            name="type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classtype",
            ),
        ),
    ]
