# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0004_auto_20160304_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlocation',
            name='sensor_ref',
            field=models.ForeignKey(blank=True, to='datamodel.Sensor', null=True),
        ),
    ]
