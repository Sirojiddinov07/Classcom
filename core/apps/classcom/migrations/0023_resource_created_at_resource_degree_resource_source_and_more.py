# Generated by Django 5.0.7 on 2024-08-15 06:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0022_resource_subtype_alter_resourcetype_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resource",
            name="degree",
            field=models.CharField(
                choices=[
                    ("LOW", "Past"),
                    ("MEDIUM", "O'rta"),
                    ("HIGH", "Yuqori"),
                ],
                default="MEDIUM",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="source",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="resource",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
    ]
