# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotlaunchpad_tfl', '0005_auto_20151211_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busstop',
            name='naptan_id',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='busstopgroup',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
