# Generated by Django 5.0.8 on 2024-08-30 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0078_alter_scheduletemplate_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="resourcetype",
            options={
                "ordering": ["order_number"],
                "verbose_name": "Resurs turi",
                "verbose_name_plural": "Resurs turlari",
            },
        ),
    ]
