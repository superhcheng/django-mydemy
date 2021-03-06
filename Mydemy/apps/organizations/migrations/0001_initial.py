# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-06-08 03:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='City Name')),
                ('desc', models.CharField(max_length=200, verbose_name='City Description')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='City Created Time')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Organization Name')),
                ('desc', models.CharField(max_length=200, verbose_name='Organization Description')),
                ('fav_count', models.IntegerField(default=0, verbose_name='Favourite Count')),
                ('click_count', models.IntegerField(default=0, verbose_name='Click Count')),
                ('image', models.ImageField(upload_to='organizations/org/%Y/%m', verbose_name='Organization Profile Picture')),
                ('address', models.CharField(max_length=200, verbose_name='Organization Address')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='Organization Created Time')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.City', verbose_name='Organization based City')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Instructor Name')),
                ('work_year', models.IntegerField(default=0, verbose_name='Year(s) of Working Experience')),
                ('curr_company', models.CharField(max_length=50, verbose_name='Current Company')),
                ('curr_title', models.CharField(max_length=50, verbose_name='Title')),
                ('point', models.IntegerField(default=0, verbose_name='Point')),
                ('fav_count', models.IntegerField(default=0, verbose_name='Favourite Count')),
                ('click_count', models.IntegerField(default=0, verbose_name='Click Count')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='Instructor Created Time')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='Organization')),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
        ),
    ]
