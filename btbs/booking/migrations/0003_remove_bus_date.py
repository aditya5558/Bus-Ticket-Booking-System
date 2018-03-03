# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_wallet_four_digit_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='date',
        ),
    ]
