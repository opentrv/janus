# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('type', models.CharField(max_length=50, null=True, blank=True)),
                ('value', models.CharField(max_length=50, null=True, blank=True)),
                ('value_integer', models.IntegerField(null=True, blank=True)),
                ('value_float', models.FloatField(null=True, blank=True)),
                ('unit', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.RenameField(
            model_name='location',
            old_name='latlong',
            new_name='location_description',
        ),
        migrations.RenameField(
            model_name='sensormetadata',
            old_name='Sensor_id',
            new_name='node_id',
        ),
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='location',
            name='location',
        ),
        migrations.RemoveField(
            model_name='location',
            name='location_decription',
        ),
        migrations.RemoveField(
            model_name='location',
            name='parent_location',
        ),
        migrations.RemoveField(
            model_name='location',
            name='room',
        ),
        migrations.RemoveField(
            model_name='location',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='location',
            name='wall',
        ),
        migrations.RemoveField(
            model_name='sensorlocation',
            name='sensor_id',
        ),
        migrations.AddField(
            model_name='location',
            name='parentId',
            field=models.ForeignKey(related_name='children', blank=True, to='datamodel.Location', null=True),
        ),
        migrations.AddField(
            model_name='sensormetadata',
            name='unit',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address_ref',
            field=models.ForeignKey(blank=True, to='datamodel.Address', null=True),
        ),
        migrations.AlterField(
            model_name='sensorlocation',
            name='sensor_ref',
            field=models.ForeignKey(blank=True, to='datamodel.SensorMetaData', null=True),
        ),
        migrations.AlterField(
            model_name='sensorlocation',
            name='timestamp_finish',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sensormetadata',
            name='type',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='sensormetadata',
            name='value',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='measurement2',
            name='sensor_location_reference',
            field=models.ForeignKey(blank=True, to='datamodel.SensorLocation', null=True),
        ),
    ]
