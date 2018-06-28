# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0003_auto_20180625_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duplicate',
            field=models.IntegerField(default=1),
        ),
    ]
