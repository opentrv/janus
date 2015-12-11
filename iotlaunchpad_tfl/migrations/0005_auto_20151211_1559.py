# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotlaunchpad_tfl', '0004_busstoptobusstopgroup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='busstoptobusstopgroup',
            unique_together=set([('bus_stop', 'bus_stop_group')]),
        ),
    ]
