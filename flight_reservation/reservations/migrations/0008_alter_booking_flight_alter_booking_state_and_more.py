# Generated by Django 5.1.3 on 2024-12-13 22:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_alter_booking_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.flight'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='state',
            field=models.CharField(default='PendingState', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
