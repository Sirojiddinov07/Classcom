# Generated by Django 5.0.8 on 2024-09-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("http", "0007_alter_user_status_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="status",
            field=models.BooleanField(
                default=False, verbose_name="Shartnoma statusi"
            ),
        ),
    ]
