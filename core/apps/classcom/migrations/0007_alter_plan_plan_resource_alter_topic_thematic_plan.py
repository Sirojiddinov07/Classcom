# Generated by Django 5.0.7 on 2024-07-22 18:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "classcom",
            "0006_classes_name_en_classes_name_ru_classes_name_uz_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="plan_resource",
            field=models.ManyToManyField(blank=True, to="classcom.media"),
        ),
        migrations.AlterField(
            model_name="topic",
            name="thematic_plan",
            field=models.ManyToManyField(
                blank=True, related_name="topics", to="classcom.plan"
            ),
        ),
    ]
