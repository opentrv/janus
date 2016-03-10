# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0007_auto_20160310_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='packet_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
