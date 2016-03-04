# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0003_auto_20160304_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensormetadata',
            name='sensor_ref',
            field=models.ForeignKey(default=b'undefined', to='datamodel.Sensor'),
        ),
    ]
