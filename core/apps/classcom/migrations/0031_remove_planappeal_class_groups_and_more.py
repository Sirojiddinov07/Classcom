# Generated by Django 5.0.8 on 2024-10-28 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0030_alter_moderator_degree"),
        ("http", "0010_remove_user_science_group_user_science_group"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="planappeal",
            name="class_groups",
        ),
        migrations.RemoveField(
            model_name="planappeal",
            name="classes",
        ),
        migrations.RemoveField(
            model_name="planappeal",
            name="docs",
        ),
        migrations.RemoveField(
            model_name="planappeal",
            name="science",
        ),
        migrations.RemoveField(
            model_name="planappeal",
            name="science_type",
        ),
        migrations.RemoveField(
            model_name="planappeal",
            name="user",
        ),
        migrations.AlterField(
            model_name="tmrfiles",
            name="file",
            field=models.FileField(
                upload_to="tmr/%Y/%m/%d/", verbose_name="Fayl"
            ),
        ),
        migrations.CreateModel(
            name="TMRAppeal",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Kutilmoqda"),
                            ("accepted", "Qabul qilindi"),
                            ("rejected", "Rad etildi"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Holat",
                    ),
                ),
                (
                    "class_groups",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="http.classgroup",
                        verbose_name="Sinflar turlari",
                    ),
                ),
                (
                    "classes",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="classcom.classes",
                        verbose_name="Sinflar",
                    ),
                ),
                (
                    "science",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="classcom.science",
                        verbose_name="Fan",
                    ),
                ),
                (
                    "science_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="classcom.sciencetypes",
                        verbose_name="Fan turi",
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
            ],
            options={
                "verbose_name": "TMR arizalari",
                "verbose_name_plural": "TMR arizalari",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddField(
            model_name="tmrfiles",
            name="tmr_appeal",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="classcom.tmrappeal",
                verbose_name="TMR",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="ChangeModerator",
        ),
        migrations.DeleteModel(
            name="PlanAppeal",
        ),
    ]
