# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conrec', '0004_auto_20150709_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='name',
            field=models.CharField(default='Default', max_length=60),
            preserve_default=False,
        ),
    ]
