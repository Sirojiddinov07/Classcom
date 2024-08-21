# Generated by Django 5.1 on 2024-08-21 06:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0035_resource_order_number"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="schedule",
            unique_together={("start_time", "end_time", "user")},
        ),
        migrations.AddField(
            model_name="schedule",
            name="name",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Dars jadvali nomi",
            ),
        ),
        migrations.CreateModel(
            name="Weeks",
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
                (
                    "week_count",
                    models.IntegerField(verbose_name="Hafta raqami"),
                ),
                (
                    "start_date",
                    models.DateField(
                        verbose_name="Haftaning boshlanish sanasi"
                    ),
                ),
                (
                    "end_date",
                    models.DateField(verbose_name="Haftaning tugash sanasi"),
                ),
                (
                    "quarter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classcom.quarter",
                        verbose_name="Chorak",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hafta",
                "verbose_name_plural": "Haftalar",
            },
        ),
        migrations.RemoveField(
            model_name="schedule",
            name="date",
        ),
        migrations.RemoveField(
            model_name="schedule",
            name="quarter",
        ),
        migrations.CreateModel(
            name="ScheduleChoices",
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
                (
                    "quarter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classcom.quarter",
                        verbose_name="Chorak",
                    ),
                ),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classcom.schedule",
                        verbose_name="Dars jadvali",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Foydalanuvchi",
                    ),
                ),
                (
                    "week",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classcom.weeks",
                        verbose_name="Hafta",
                    ),
                ),
            ],
            options={
                "verbose_name": "Dars jadvali tanlash",
                "verbose_name_plural": "Dars jadvali tanlash",
                "unique_together": {("schedule", "user")},
            },
        ),
    ]
