# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0002_auto_20180625_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.CharField(max_length=40, default='0', choices=[('0', '未审批'), ('1', '已审批')]),
        ),
    ]
