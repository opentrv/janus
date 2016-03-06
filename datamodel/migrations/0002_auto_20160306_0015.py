# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
