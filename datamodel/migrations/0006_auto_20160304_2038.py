# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0005_auto_20160304_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='post_code',
            new_name='postcode',
        ),
        migrations.RenameField(
            model_name='measurement',
            old_name='sensor_location_reference',
            new_name='sensor_location_ref',
        ),
        migrations.RenameField(
            model_name='sensormetadata',
            old_name='type',
            new_name='sensor_type',
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='sensorlocation',
            name='finish',
            field=models.DateTimeField(null=True),
        ),
    ]
