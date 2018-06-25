# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duplicate',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='attrib',
            name='picture',
            field=models.ImageField(null=True, upload_to='basicInfo/static/basicInfo/picture'),
        ),
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.CharField(max_length=40, default='0', choices=[('0', '未审批'), ('1', '已审批')]),
        ),
    ]
