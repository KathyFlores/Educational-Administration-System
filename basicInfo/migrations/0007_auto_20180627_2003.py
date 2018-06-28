# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0006_course_exam_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teach',
            name='duplicate',
            field=models.IntegerField(null=True),
        ),
    ]
