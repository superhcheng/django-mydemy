# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-07-13 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_instructor_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='point',
        ),
        migrations.AddField(
            model_name='instructor',
            name='specialty',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Specialty'),
        ),
    ]
