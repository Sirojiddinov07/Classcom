# Generated by Django 5.0.8 on 2024-10-10 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0017_rename_type_download_object_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="media",
            old_name="object_type_id",
            new_name="object_id",
        ),
    ]
