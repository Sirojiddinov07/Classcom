# Generated by Django 5.0.1 on 2024-09-12 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0010_schedule_science_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tempmoderator",
            name="science",
        ),
        migrations.RemoveField(
            model_name="tempmoderator",
            name="science_type",
        ),
    ]
