# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conrec', '0003_auto_20150619_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendationmatrix',
            name='data',
            field=models.CharField(max_length=8192),
            preserve_default=True,
        ),
    ]
