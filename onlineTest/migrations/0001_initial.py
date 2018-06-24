# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('chapter', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField()),
                ('choice_a', models.TextField()),
                ('choice_b', models.TextField()),
                ('choice_c', models.TextField()),
                ('choice_d', models.TextField()),
                ('solution', models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])),
                ('score', models.PositiveSmallIntegerField(default=1)),
                ('add_time', models.DateTimeField(verbose_name='time added')),
                ('latest_modify_time', models.DateTimeField(verbose_name='time latest modified')),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceQuestionAnswerRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('answer', models.CharField(max_length=1, blank=True, null=True, default=None, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])),
                ('answer_time', models.DateTimeField(verbose_name='time answered', blank=True, null=True, default=None)),
                ('question', models.ForeignKey(to='onlineTest.ChoiceQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='KnowledgePoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('knowledge_point', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('class_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField(verbose_name='date starts')),
                ('end_time', models.DateTimeField(verbose_name='date ends')),
                ('attend_students', models.ManyToManyField(blank=True, null=True, to='onlineTest.Student')),
                ('choice_questions', models.ManyToManyField(blank=True, null=True, to='onlineTest.ChoiceQuestion')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Teacher')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='TrueOrFalseQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField()),
                ('solution', models.BooleanField()),
                ('score', models.PositiveSmallIntegerField(default=1)),
                ('add_time', models.DateTimeField(verbose_name='time added')),
                ('latest_modify_time', models.DateTimeField(verbose_name='time latest modified')),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Chapter')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Teacher')),
                ('knowledge_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.KnowledgePoint')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='TrueOrFalseQuestionAnswerRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('answer', models.NullBooleanField(default=None)),
                ('answer_time', models.DateTimeField(verbose_name='time answered', default=None)),
                ('question', models.ForeignKey(to='onlineTest.TrueOrFalseQuestion')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Student')),
                ('test', models.ForeignKey(to='onlineTest.Test')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='true_or_false_questions',
            field=models.ManyToManyField(blank=True, null=True, to='onlineTest.TrueOrFalseQuestion'),
        ),
        migrations.AddField(
            model_name='choicequestionanswerrecord',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Student'),
        ),
        migrations.AddField(
            model_name='choicequestionanswerrecord',
            name='test',
            field=models.ForeignKey(to='onlineTest.Test'),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Teacher'),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='knowledge_point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.KnowledgePoint'),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlineTest.Subject'),
        ),
    ]
