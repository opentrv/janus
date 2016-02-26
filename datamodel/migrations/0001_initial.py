# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=300, blank=True)),
                ('post_code', models.CharField(max_length=20, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_location', models.CharField(max_length=50, blank=True)),
                ('location', models.CharField(max_length=32, blank=True)),
                ('location_decription', models.CharField(max_length=50, blank=True)),
                ('latlong', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=300, blank=True)),
                ('floor', models.IntegerField(blank=True)),
                ('room', models.IntegerField(blank=True)),
                ('wall', models.CharField(max_length=20, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('address_ref', models.ForeignKey(to='datamodel.Address')),
            ],
        ),
        migrations.CreateModel(
            name='SensorLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensor_id', models.CharField(max_length=50)),
                ('aes_key', models.CharField(max_length=256, blank=True)),
                ('timestamp_start', models.DateTimeField(auto_now_add=True, null=True)),
                ('timestamp_finish', models.DateTimeField(blank=True)),
                ('timestamp_updated', models.DateTimeField(auto_now=True, null=True)),
                ('sensor_location', models.ForeignKey(blank=True, to='datamodel.Location', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Sensor_id', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20)),
                ('value', models.FloatField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='sensor_ref',
            field=models.ForeignKey(to='datamodel.SensorMetaData'),
        ),
    ]
