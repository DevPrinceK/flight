# Generated by Django 4.1 on 2022-09-12 22:54

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_code',
            field=models.CharField(default=backend.models.Booking.generate_ticket_id, max_length=255),
        ),
    ]
