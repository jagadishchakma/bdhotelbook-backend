# Generated by Django 5.0.6 on 2024-07-11 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0014_hotelreview_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='hotelreview',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
