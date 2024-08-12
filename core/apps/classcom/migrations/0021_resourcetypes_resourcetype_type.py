# Generated by Django 5.0.7 on 2024-08-12 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0020_remove_moderator_science_group_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResourceTypes",
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
                ("name", models.CharField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("BYLIST", "By list"),
                            ("BYCLASS", "By class"),
                            ("BYCLASSANDUNIT", "By class and unit"),
                            ("BYCLASSOUT", "By class out"),
                            ("BYDOCS", "By docs"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="resourcetype",
            name="type",
            field=models.CharField(
                choices=[
                    ("BYLIST", "By list"),
                    ("BYCLASS", "By class"),
                    ("BYCLASSANDUNIT", "By class and unit"),
                    ("BYCLASSOUT", "By class out"),
                    ("BYDOCS", "By docs"),
                ],
                default=1,
            ),
            preserve_default=False,
        ),
    ]
