# Generated by Django 5.0.4 on 2024-04-29 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classcom', '0006_feedback_answer_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='answered',
            new_name='is_answered',
        ),
    ]
