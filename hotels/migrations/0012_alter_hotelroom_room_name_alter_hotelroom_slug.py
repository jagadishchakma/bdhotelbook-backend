# Generated by Django 5.0.6 on 2024-07-10 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0011_hotelroom_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelroom',
            name='room_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='hotelroom',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
