# Generated by Django 5.0.8 on 2024-08-22 10:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                ("message", models.TextField(verbose_name="Xabar")),
                (
                    "message_uz",
                    models.TextField(null=True, verbose_name="Xabar"),
                ),
                (
                    "message_ru",
                    models.TextField(null=True, verbose_name="Xabar"),
                ),
                (
                    "message_en",
                    models.TextField(null=True, verbose_name="Xabar"),
                ),
                (
                    "is_read",
                    models.BooleanField(
                        default=False, verbose_name="O'qilgan"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Foydalanuvchi",
                    ),
                ),
            ],
            options={
                "verbose_name": "Bildirishnoma",
                "verbose_name_plural": "Bildirishnomalar",
                "db_table": "notification",
            },
        ),
    ]
