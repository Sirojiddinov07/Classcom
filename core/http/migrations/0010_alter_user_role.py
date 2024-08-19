# Generated by Django 5.0.6 on 2024-06-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("http", "0009_alter_district_region"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Administrator"),
                    ("moderator", "Moderator"),
                    ("user", "User"),
                ],
                default="user",
                max_length=255,
            ),
        ),
    ]
