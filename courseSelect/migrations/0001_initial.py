# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='creditNeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('elective', models.FloatField()),
                ('public', models.FloatField()),
                ('discipline', models.ForeignKey(unique=True, to='basicInfo.discipline')),
            ],
        ),
        migrations.CreateModel(
            name='curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('courses', models.ManyToManyField(null=True, related_name='course_curriculum', to='basicInfo.course')),
                ('student', models.ForeignKey(to='basicInfo.student')),
            ],
        ),
        migrations.CreateModel(
            name='requiredCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('discipline', models.ForeignKey(to='basicInfo.discipline')),
                ('required_courses', models.ManyToManyField(null=True, related_name='required_course', to='basicInfo.course')),
            ],
        ),
        migrations.CreateModel(
            name='selectControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('max_connections', models.IntegerField(default=500)),
            ],
        ),
        migrations.CreateModel(
            name='selection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('select_time', models.DateTimeField(null=True)),
                ('priority', models.IntegerField()),
                ('state', models.BooleanField()),
                ('student', models.ForeignKey(to='basicInfo.student')),
                ('teach', models.ForeignKey(to='basicInfo.teach')),
            ],
        ),
        migrations.CreateModel(
            name='timeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='selectcontrol',
            name='apply_time',
            field=models.ForeignKey(related_name='apply_time', to='courseSelect.timeSlot'),
        ),
        migrations.AddField(
            model_name='selectcontrol',
            name='first_time',
            field=models.ForeignKey(related_name='first_time', to='courseSelect.timeSlot'),
        ),
        migrations.AddField(
            model_name='selectcontrol',
            name='withdraw_time',
            field=models.ForeignKey(to='courseSelect.timeSlot'),
        ),
    ]
