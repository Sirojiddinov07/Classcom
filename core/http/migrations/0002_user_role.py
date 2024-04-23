# Generated by Django 5.0.4 on 2024-04-23 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('http', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('superuser', 'Superuser'), ('admin', 'Admin'), ('user', 'User')], default='user', max_length=255),
        ),
    ]
