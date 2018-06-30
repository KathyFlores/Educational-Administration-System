# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineTest', '0002_auto_20180629_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='subjects',
        ),
        migrations.AlterField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.course'),
        ),
        migrations.AlterField(
            model_name='choicequestion',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.teacher'),
        ),
        migrations.AlterField(
            model_name='choicequestion',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.course'),
        ),
        migrations.AlterField(
            model_name='choicequestionanswerrecord',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.student'),
        ),
        migrations.AlterField(
            model_name='knowledgepoint',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.course'),
        ),
        migrations.AlterField(
            model_name='test',
            name='attend_students',
            field=models.ManyToManyField(blank=True, null=True, to='basicInfo.student'),
        ),
        migrations.AlterField(
            model_name='test',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.teacher'),
        ),
        migrations.AlterField(
            model_name='test',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.course'),
        ),
        migrations.AlterField(
            model_name='trueorfalsequestion',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.teacher'),
        ),
        migrations.AlterField(
            model_name='trueorfalsequestion',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.course'),
        ),
        migrations.AlterField(
            model_name='trueorfalsequestionanswerrecord',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.student'),
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
