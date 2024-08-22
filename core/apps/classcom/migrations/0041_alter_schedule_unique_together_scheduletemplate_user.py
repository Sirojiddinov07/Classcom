# Generated by Django 5.0.8 on 2024-08-22 05:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0040_alter_schedulechoices_unique_together_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="schedule",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="scheduletemplate",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
            preserve_default=False,
        ),
    ]
