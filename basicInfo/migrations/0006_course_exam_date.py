# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='exam_date',
            field=models.DateField(null=True),
        ),
    ]
