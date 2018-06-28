# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0009_auto_20180627_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='exam_date',
            field=models.DateTimeField(null=True),
        ),
    ]
