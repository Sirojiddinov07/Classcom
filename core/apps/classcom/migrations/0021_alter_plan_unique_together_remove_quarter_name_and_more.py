# Generated by Django 5.0.6 on 2024-06-15 05:42

import core.apps.classcom.models.schedule
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classcom", "0020_schedule_lesson_time_schedule_quarter"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quarter",
            name="name",
        ),
        migrations.AddField(
            model_name="quarter",
            name="choices",
            field=models.IntegerField(
                choices=[
                    (1, "First Quarter"),
                    (2, "Second Quarter"),
                    (3, "Third Quarter"),
                    (4, "Fourth Quarter"),
                ],
                default=1,
            ),
        ),
        migrations.AddField(
            model_name="quarter",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime.today
            ),
        ),
        migrations.AddField(
            model_name="quarter",
            name="start_date",
            field=models.DateField(
                blank=True, default=datetime.datetime.today
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="weekday",
            field=models.CharField(
                choices=[
                    ("monday", "Monday"),
                    ("tuesday", "Tuesday"),
                    ("wednesday", "Wednesday"),
                    ("thursday", "Thursday"),
                    ("friday", "Friday"),
                    ("saturday", "Saturday"),
                ],
                max_length=15,
            ),
        ),
    ]
