# Generated by Django 5.1.3 on 2024-12-09 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0005_alter_booking_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="loyalty_points",
            field=models.IntegerField(default=0),
        ),
    ]
