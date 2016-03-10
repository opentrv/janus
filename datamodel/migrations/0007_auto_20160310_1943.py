# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0006_auto_20160310_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
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
            options={
                'permissions': (('view_measurement', 'Can see measurements'),),
            },
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='measurement_type',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='value',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='value_float',
        ),
        migrations.RemoveField(
            model_name='measurement',
            name='value_integer',
        ),
        migrations.AddField(
            model_name='measurement',
            name='message_counter',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='packet_timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reading',
            name='measurement_ref',
            field=models.ForeignKey(verbose_name=b'measurement', to='datamodel.Measurement'),
        ),
    ]
