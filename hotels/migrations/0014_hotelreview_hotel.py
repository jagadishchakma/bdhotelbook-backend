# Generated by Django 5.0.6 on 2024-07-11 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_alter_hotels_rooms_hotelreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelreview',
            name='hotel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotel_review', to='hotels.hotels'),
        ),
    ]