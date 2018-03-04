# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20180303_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfeedback',
            name='subject',
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='booking',
            field=models.ForeignKey(to='booking.Booking', null=True),
        ),
    ]
