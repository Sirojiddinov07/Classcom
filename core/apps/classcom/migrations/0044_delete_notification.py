# Generated by Django 5.0.8 on 2024-08-22 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "classcom",
            "0043_alter_classtype_options_alter_classes_type_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="Notification",
        ),
    ]
