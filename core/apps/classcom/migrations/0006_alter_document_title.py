# Generated by Django 5.0.8 on 2024-09-07 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0005_document_alter_languagemodel_language_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="title",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Title"
            ),
        ),
    ]
