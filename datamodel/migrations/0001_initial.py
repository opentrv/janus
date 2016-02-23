# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Sensor_id', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300, blank=True)),
                ('floor', models.IntegerField(blank=True)),
                ('room', models.IntegerField(blank=True)),
                ('wall', models.CharField(max_length=20, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
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
    ]
