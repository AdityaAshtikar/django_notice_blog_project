# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-02 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20180202_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='topic',
            field=models.CharField(blank=True, default='Event', max_length=100),
        ),
    ]
