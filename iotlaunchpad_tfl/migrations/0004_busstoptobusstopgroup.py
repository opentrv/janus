# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotlaunchpad_tfl', '0003_busstopgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusStopToBusStopGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bus_stop', models.ForeignKey(to='iotlaunchpad_tfl.BusStop')),
                ('bus_stop_group', models.ForeignKey(to='iotlaunchpad_tfl.BusStopGroup')),
            ],
        ),
    ]
