# Generated by Django 5.0.7 on 2024-08-12 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_payments_status_alter_orders_end_date_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="orders",
            options={
                "verbose_name": "Orders",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.AlterModelOptions(
            name="payments",
            options={
                "verbose_name": "Payments",
                "verbose_name_plural": "Payments",
            },
        ),
        migrations.AlterModelOptions(
            name="plans",
            options={"verbose_name": "Plans", "verbose_name_plural": "Plans"},
        ),
    ]
