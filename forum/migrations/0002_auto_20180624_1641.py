# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='author',
            field=models.ForeignKey(to='basicInfo.attrib'),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(related_name='receiver', to='basicInfo.attrib'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='sender', to='basicInfo.attrib'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='basicInfo.attrib'),
        ),
        migrations.AlterField(
            model_name='post',
            name='last_replied_by',
            field=models.ForeignKey(blank=True, null=True, related_name='post_last', to='basicInfo.attrib'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(to='basicInfo.attrib'),
        ),
    ]
