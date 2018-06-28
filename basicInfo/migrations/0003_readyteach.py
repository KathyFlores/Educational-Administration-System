# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0002_auto_20180625_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='readyteach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('capacity', models.IntegerField()),
                ('course_id', models.ForeignKey(to='basicInfo.course')),
                ('teacher_id', models.ForeignKey(to='basicInfo.teacher')),
            ],
        ),
    ]
