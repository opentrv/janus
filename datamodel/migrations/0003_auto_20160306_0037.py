# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0002_auto_20160306_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
