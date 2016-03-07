# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0004_auto_20160306_0039'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'permissions': (('view_measurement', 'Can see measurements'),)},
        ),
    ]
