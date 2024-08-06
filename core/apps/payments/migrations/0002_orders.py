# Generated by Django 5.0.7 on 2024-08-05 12:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0017_delete_orders"),
        ("payments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
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
                (
                    "start_date",
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("price", models.BigIntegerField(default=0)),
                ("status", models.BooleanField(default=False)),
                (
                    "science",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classcom.science",
                    ),
                ),
                ("types", models.ManyToManyField(to="classcom.sciencetypes")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Orders",
                "verbose_name_plural": "Orderss",
            },
        ),
    ]
