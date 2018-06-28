# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0008_auto_20180627_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teach',
            name='duplicate',
        ),
        migrations.RemoveField(
            model_name='teach',
            name='exam_date',
        ),
    ]
