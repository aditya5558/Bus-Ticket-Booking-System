# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_remove_booking_booking_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='num_seats',
            field=models.IntegerField(null=True),
        ),
    ]
