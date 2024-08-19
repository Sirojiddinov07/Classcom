# Generated by Django 5.0.7 on 2024-08-09 07:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("classcom", "0020_remove_moderator_science_group_and_more"),
        ("payments", "0003_payments_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="payments",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="payments",
            name="price",
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="payments",
            name="trans_id",
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="payments",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="Plans",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.BigIntegerField(default=0)),
                (
                    "quarter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classcom.quarter",
                    ),
                ),
            ],
        ),
    ]
