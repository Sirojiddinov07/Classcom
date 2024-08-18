# Generated by Django 5.1 on 2024-08-18 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0028_classtype_classes_type"),
    ]

    operations = [
        migrations.AlterField(
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
