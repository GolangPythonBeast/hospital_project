# Generated by Django 5.2.3 on 2025-07-21 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_rename_notification_patient_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 7, 21, 12, 34, 36, 930192, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
