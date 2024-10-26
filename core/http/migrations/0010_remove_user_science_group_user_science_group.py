# Generated by Django 5.0.8 on 2024-10-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0030_alter_moderator_degree"),
        ("http", "0009_user_father_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="science_group",
        ),
        migrations.AddField(
            model_name="user",
            name="science_group",
            field=models.ManyToManyField(
                blank=True,
                to="classcom.sciencetypes",
                verbose_name="Fanlar turlari",
            ),
        ),
    ]
