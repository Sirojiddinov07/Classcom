# Generated by Django 5.0.8 on 2024-08-22 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0042_alter_schedule_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="classtype",
            options={
                "verbose_name": "Sinf Guruhi",
                "verbose_name_plural": "Sinf Guruhlari",
            },
        ),
        migrations.AlterField(
            model_name="classes",
            name="type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classtype",
                verbose_name="Sinf guruhi",
            ),
        ),
        migrations.AlterField(
            model_name="classtype",
            name="name",
            field=models.CharField(
                max_length=255, verbose_name="Sinf guruhi nomi"
            ),
        ),
        migrations.AlterField(
            model_name="classtype",
            name="name_en",
            field=models.CharField(
                max_length=255, null=True, verbose_name="Sinf guruhi nomi"
            ),
        ),
        migrations.AlterField(
            model_name="classtype",
            name="name_ru",
            field=models.CharField(
                max_length=255, null=True, verbose_name="Sinf guruhi nomi"
            ),
        ),
        migrations.AlterField(
            model_name="classtype",
            name="name_uz",
            field=models.CharField(
                max_length=255, null=True, verbose_name="Sinf guruhi nomi"
            ),
        ),
    ]
