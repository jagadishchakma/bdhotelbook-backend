# Generated by Django 5.0.6 on 2024-07-10 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_hotelroom_room_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]