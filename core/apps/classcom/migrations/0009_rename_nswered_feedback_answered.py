# Generated by Django 5.0.4 on 2024-04-29 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classcom', '0008_rename_is_answered_feedback_nswered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='nswered',
            new_name='answered',
        ),
    ]
