# Generated by Django 5.0.6 on 2024-06-20 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0023_media_desc_alter_schedule_lesson_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="quarter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.quarter",
            ),
        ),
    ]
