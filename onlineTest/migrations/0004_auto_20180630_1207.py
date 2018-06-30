# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineTest', '0003_auto_20180630_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trueorfalsequestionanswerrecord',
            name='answer_time',
            field=models.DateTimeField(verbose_name='time answered', blank=True, null=True, default=None),
        ),
    ]
