# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-07-07 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20190707_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_notes',
            field=models.CharField(default='', max_length=500, verbose_name='Course Notes'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_objectives',
            field=models.CharField(default='', max_length=500, verbose_name='Course Objectives'),
        ),
    ]
