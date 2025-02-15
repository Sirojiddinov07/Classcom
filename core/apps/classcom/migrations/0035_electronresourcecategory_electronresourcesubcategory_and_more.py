# Generated by Django 5.0.8 on 2025-01-27 09:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0034_alter_moderator_degree"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ElectronResourceCategory",
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
                    "name",
                    models.CharField(max_length=255, verbose_name="Name"),
                ),
                (
                    "name_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "description_uz",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Is Active"
                    ),
                ),
            ],
            options={
                "verbose_name": "Electron Resource",
                "verbose_name_plural": "Electron Resources",
            },
        ),
        migrations.CreateModel(
            name="ElectronResourceSubCategory",
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
                    "name",
                    models.CharField(max_length=255, verbose_name="Name"),
                ),
                (
                    "name_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "description_uz",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "description_ru",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "description_en",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Is Active"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_categories",
                        to="classcom.electronresourcecategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Electron Resource Sub Category",
                "verbose_name_plural": "Electron Resource Sub Categories",
            },
        ),
        migrations.CreateModel(
            name="ElectronResource",
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
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="electron_resources/", verbose_name="File"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Name"),
                ),
                (
                    "size",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Size",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Type",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Is Active"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources",
                        to="classcom.electronresourcesubcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Electron Resource File",
                "verbose_name_plural": "Electron Resource Files",
                "db_table": "electron_resource_files",
                "ordering": ["-created_at"],
            },
        ),
    ]
