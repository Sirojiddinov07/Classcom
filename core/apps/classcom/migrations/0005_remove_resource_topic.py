# Generated by Django 5.0.6 on 2024-07-02 06:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("classcom", "0004_plan_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resource",
            name="topic",
        ),
    ]
