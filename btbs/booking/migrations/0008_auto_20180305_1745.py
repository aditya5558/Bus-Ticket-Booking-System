# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20180305_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='bus_type',
            field=models.CharField(max_length=10, choices=[(b'AC', b'AC'), (b'Non AC', b'Non AC')]),
        ),
    ]
