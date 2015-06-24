# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conrec', '0002_area_keys_recommendationmatrix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendationmatrix',
            name='data',
            field=models.CharField(max_length=1024),
            preserve_default=True,
        ),
    ]
