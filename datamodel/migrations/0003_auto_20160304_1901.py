# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0002_auto_20160303_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('measurement_type', models.CharField(max_length=50, null=True, blank=True)),
                ('value', models.CharField(max_length=50, null=True, blank=True)),
                ('value_integer', models.IntegerField(null=True, blank=True)),
                ('value_float', models.FloatField(null=True, blank=True)),
                ('unit', models.CharField(max_length=50, null=True, blank=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_id', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='measurement2',
            name='sensor_location_reference',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='location_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='parentId',
            new_name='parent_ref',
        ),
        migrations.RenameField(
            model_name='sensorlocation',
            old_name='timestamp_start',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='sensorlocation',
            old_name='timestamp_finish',
            new_name='finish',
        ),
        migrations.RenameField(
            model_name='sensorlocation',
            old_name='sensor_location',
            new_name='location_ref',
        ),
        migrations.RenameField(
            model_name='sensormetadata',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='sensorlocation',
            name='timestamp_updated',
        ),
        migrations.RemoveField(
            model_name='sensormetadata',
            name='node_id',
        ),
        migrations.AddField(
            model_name='location',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='last_measurement',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='sensorlocation',
            name='sensor_ref',
            field=models.ForeignKey(blank=True, to='datamodel.SensorMetadata', null=True),
        ),
        migrations.DeleteModel(
            name='Measurement2',
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_location_reference',
            field=models.ForeignKey(blank=True, to='datamodel.SensorLocation', null=True),
        ),
        migrations.AddField(
            model_name='sensormetadata',
            name='sensor_ref',
            field=models.ForeignKey(default=2, to='datamodel.Sensor'),
            preserve_default=False,
        ),
    ]
