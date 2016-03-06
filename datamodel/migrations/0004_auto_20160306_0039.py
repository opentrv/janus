# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0003_auto_20160306_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensormetadata',
            name='sensor_type',
            field=models.CharField(max_length=50, verbose_name=b'type', blank=True),
        ),
    ]
