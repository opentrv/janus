# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opentrv_sensor', '0002_auto_20151113_1528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'permissions': (('view_measurement', 'Can see measurements'),)},
        ),
    ]
