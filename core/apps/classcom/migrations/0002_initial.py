# Generated by Django 5.0.8 on 2024-09-17 07:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("classcom", "0001_initial"),
        ("http", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="classes",
            name="type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classtype",
                verbose_name="Sinf guruhi",
            ),
        ),
        migrations.AddField(
            model_name="daysoff",
            name="_class",
            field=models.ManyToManyField(
                to="classcom.classes", verbose_name="Sinflar"
            ),
        ),
        migrations.AddField(
            model_name="daysoff",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="days_off",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="download",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="downloadtoken",
            name="download",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.download",
                verbose_name="Yuklama",
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbacks",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="feedback",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="classcom.feedback",
                verbose_name="Fikr-mulohaza",
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="download_users",
            field=models.ManyToManyField(
                blank=True,
                related_name="downloaded_media",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Yuklab olganlar",
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="media",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="download",
            name="media",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.media",
                verbose_name="Media",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="class_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="moderators",
                to="http.classgroup",
                verbose_name="Sinflar turlari",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="classes",
            field=models.ManyToManyField(
                blank=True,
                related_name="moderators",
                to="classcom.classes",
                verbose_name="Sinflar",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="docs",
            field=models.ManyToManyField(
                blank=True,
                related_name="moderators",
                to="classcom.document",
                verbose_name="Hujjatlar",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="languages",
            field=models.ManyToManyField(
                blank=True,
                related_name="moderators",
                to="classcom.languagemodel",
                verbose_name="Tillar",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="class_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="http.classgroup",
                verbose_name="Sinflar guruhi",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="classes",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classes",
                verbose_name="Sinflar",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="quarter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.quarter",
                verbose_name="Chorak",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="quarters",
            field=models.ManyToManyField(
                blank=True,
                related_name="moderators",
                to="classcom.quarter",
                verbose_name="Choraklar",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.category",
                verbose_name="Kategoriya",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="category_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.categorytype",
                verbose_name="Kategoriya turi",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="classes",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classes",
                verbose_name="Sinflar",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="media",
            field=models.ManyToManyField(
                blank=True,
                related_name="resources",
                to="classcom.media",
                verbose_name="Media",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.resourcetype",
                verbose_name="Resurs turi",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="resource_type",
            field=models.ManyToManyField(
                blank=True,
                related_name="moderators",
                to="classcom.resourcetype",
                verbose_name="Resurs turlari",
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="class_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="http.classgroup",
                verbose_name="Sinflar guruhi",
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="class_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classtype",
                verbose_name="Sinflar turi",
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="classes",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.classes",
                verbose_name="Sinflar",
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schedules",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="schedulechoices",
            name="quarter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.quarter",
                verbose_name="Chorak",
            ),
        ),
        migrations.AddField(
            model_name="schedulechoices",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="scheduletemplate",
            name="schedules",
            field=models.ManyToManyField(
                related_name="schedule_templates",
                to="classcom.schedule",
                verbose_name="Dars jadvalar",
            ),
        ),
        migrations.AddField(
            model_name="scheduletemplate",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="schedulechoices",
            name="schedule_template",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.scheduletemplate",
                verbose_name="Dars jadval shabloni",
            ),
        ),
        migrations.AddField(
            model_name="science",
            name="class_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="http.classgroup",
                verbose_name="Sinf turi",
            ),
        ),
        migrations.AddField(
            model_name="science",
            name="science_grp",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="http.sciencegroups",
                verbose_name="Fan guruhi",
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="science",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.science",
                verbose_name="Fan",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="science",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.science",
                verbose_name="Fan",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="science",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.science",
                verbose_name="Fan",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="science",
            field=models.ManyToManyField(
                blank=True, to="classcom.science", verbose_name="Fan"
            ),
        ),
        migrations.AddField(
            model_name="daysoff",
            name="science",
            field=models.ManyToManyField(
                to="classcom.science", verbose_name="Fanlar"
            ),
        ),
        migrations.AddField(
            model_name="science",
            name="types",
            field=models.ManyToManyField(
                to="classcom.sciencetypes", verbose_name="Fan turi"
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="science_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.sciencetypes",
                verbose_name="Fan turi",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="science_types",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.sciencetypes",
                verbose_name="Fan guruhi",
            ),
        ),
        migrations.AddField(
            model_name="moderator",
            name="science_type",
            field=models.ManyToManyField(
                blank=True, to="classcom.sciencetypes", verbose_name="Fan turi"
            ),
        ),
        migrations.AddField(
            model_name="teacher",
            name="science",
            field=models.ManyToManyField(
                blank=True, to="classcom.science", verbose_name="Fanlar"
            ),
        ),
        migrations.AddField(
            model_name="teacher",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Foydalanuvchi",
            ),
        ),
        migrations.AddField(
            model_name="topic",
            name="media",
            field=models.ManyToManyField(
                blank=True,
                related_name="topic",
                to="classcom.media",
                verbose_name="Media",
            ),
        ),
        migrations.AddField(
            model_name="plan",
            name="topic",
            field=models.ManyToManyField(
                blank=True,
                related_name="plans",
                to="classcom.topic",
                verbose_name="Mavzu",
            ),
        ),
        migrations.AddField(
            model_name="weeks",
            name="quarter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.quarter",
                verbose_name="Chorak",
            ),
        ),
        migrations.AddField(
            model_name="schedulechoices",
            name="week",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="classcom.weeks",
                verbose_name="Hafta",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="plan",
            unique_together={
                (
                    "classes",
                    "quarter",
                    "science",
                    "class_group",
                    "science_types",
                )
            },
        ),
    ]
