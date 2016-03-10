# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0005_auto_20160306_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlocation',
            name='finish',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sensorlocation',
            name='last_measurement',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
