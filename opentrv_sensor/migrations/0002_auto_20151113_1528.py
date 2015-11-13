# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('opentrv_sensor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 13, 15, 28, 1, 484317, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_id',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='type',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together=set([('datetime', 'type', 'sensor_id')]),
        ),
    ]
