# Generated by Django 5.0.8 on 2024-08-07 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("classcom", "0018_merge_0017_delete_orders_0017_merge_20240805_1753"),
        ("http", "0014_alter_smsconfirm_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="moderator",
            name="classes",
        ),
        migrations.RemoveField(
            model_name="tempmoderator",
            name="classes",
        ),
        migrations.AddField(
            model_name="moderator",
            name="science_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="http.sciencegroups",
            ),
        ),
        migrations.AddField(
            model_name="tempmoderator",
            name="science_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="http.sciencegroups",
            ),
        ),
    ]
