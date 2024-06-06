# Generated by Django 4.2.13 on 2024-06-06 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_membership_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 7, 11, 31, 57, 203935)),
        ),
    ]