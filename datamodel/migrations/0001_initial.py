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
                ('postcode', models.CharField(max_length=20, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('address_ref', models.ForeignKey(verbose_name=b'address', blank=True, to='datamodel.Address', null=True)),
                ('parent_ref', models.ForeignKey(related_name='children', blank=True, to='datamodel.Location', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('measurement_type', models.CharField(max_length=50, null=True, blank=True)),
                ('value', models.CharField(max_length=50, null=True, blank=True)),
                ('value_integer', models.IntegerField(null=True, verbose_name=b'integer value', blank=True)),
                ('value_float', models.FloatField(null=True, verbose_name=b'floating point value', blank=True)),
                ('unit', models.CharField(max_length=50, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
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
        migrations.CreateModel(
            name='SensorLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aes_key', models.CharField(max_length=256, verbose_name=b'AES key', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('last_measurement', models.DateTimeField(null=True)),
                ('finish', models.DateTimeField(null=True)),
                ('location_ref', models.ForeignKey(verbose_name=b'location', blank=True, to='datamodel.Location', null=True)),
                ('sensor_ref', models.ForeignKey(verbose_name=b'sensor', blank=True, to='datamodel.Sensor', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensor_type', models.CharField(max_length=50, blank=True)),
                ('value', models.CharField(max_length=50, blank=True)),
                ('unit', models.CharField(max_length=50, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('sensor_ref', models.ForeignKey(verbose_name=b'sensor', to='datamodel.Sensor')),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_location_ref',
            field=models.ForeignKey(verbose_name=b'sensor-location', blank=True, to='datamodel.SensorLocation', null=True),
        ),
    ]
