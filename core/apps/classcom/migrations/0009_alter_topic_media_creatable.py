# Generated by Django 5.0.8 on 2024-10-02 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0008_moderator_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="media_creatable",
            field=models.BooleanField(
                default=False, verbose_name="Resurs yarata olishi."
            ),
        ),
    ]
