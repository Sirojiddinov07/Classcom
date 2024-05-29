# Generated by Django 5.0.4 on 2024-04-26 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="classes",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classes",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="schedule",
            name="science",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="classcom.science"
            ),
        ),
    ]
