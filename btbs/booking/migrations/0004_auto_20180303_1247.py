# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_bus_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='rating',
            field=models.IntegerField(blank=True, null=True, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')]),
        ),
    ]
