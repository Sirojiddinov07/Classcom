# Generated by Django 5.0.8 on 2024-09-23 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0003_ai"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="is_answered",
            field=models.BooleanField(
                default=False, verbose_name="Javob berildi"
            ),
        ),
    ]
