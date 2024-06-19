# Generated by Django 5.0.6 on 2024-06-13 06:51

import core.apps.classcom.models.schedule
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0019_remove_plan_plan_resource_plan_plan_resource"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="quarter",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.quarter",
            ),
        ),
    ]
