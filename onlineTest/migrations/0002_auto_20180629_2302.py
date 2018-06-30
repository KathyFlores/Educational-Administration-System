# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineTest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Subject'),
        ),
        migrations.AddField(
            model_name='knowledgepoint',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, to='onlineTest.Subject'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, to='onlineTest.Subject'),
        ),
    ]
