# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotlaunchpad_tfl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='busstop',
            name='latitude',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='busstop',
            name='longitude',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='busstop',
            name='naptan_id',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='busstop',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
