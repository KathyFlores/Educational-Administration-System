# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0007_auto_20180627_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duplicate',
            field=models.IntegerField(default=0),
        ),
    ]
