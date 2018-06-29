# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='teach',
            name='duplicate',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='duplicate',
            field=models.IntegerField(default=0),
        ),
    ]
