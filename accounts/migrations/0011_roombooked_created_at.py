# Generated by Django 5.0.6 on 2024-07-12 07:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='roombooked',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]