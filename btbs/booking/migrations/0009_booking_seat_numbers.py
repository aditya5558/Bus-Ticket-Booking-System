# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20180305_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seat_numbers',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
