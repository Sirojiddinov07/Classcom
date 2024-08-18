# Generated by Django 5.1 on 2024-08-18 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0027_media_file_type"),
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
            model_name="classes",
            name="type",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classtype",
            ),
            preserve_default=False,
        ),
    ]
