from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='City Name')
    desc = models.CharField(max_length=200, verbose_name='City Description')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='City Created Time')

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __unicode__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='Organization Name')
    desc = models.CharField(max_length=200, verbose_name='Organization Description')
    category = models.CharField(max_length=30, default='college', choices=(('college', 'College'), ('institution', 'Institution'), ('individual', 'Individual')), verbose_name='Organization Category')
    fav_count = models.IntegerField(default=0, verbose_name='Favourite Count')
    click_count = models.IntegerField(default=0, verbose_name='Click Count')
    student_count = models.IntegerField(default=0, verbose_name='Student Count')
    course_count = models.IntegerField(default=0, verbose_name='Course Count')
    image = models.ImageField(upload_to='organizations/org/%Y/%m', verbose_name='Organization Profile Picture')
    address = models.CharField(max_length=200, verbose_name='Organization Address')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Organization based City')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Organization Created Time')

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


    def __unicode__(self):
        return self.name

class Instructor(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='Organization')
    name = models.CharField(max_length=50, verbose_name='Instructor Name')
    work_year = models.IntegerField(default=0, verbose_name='Year(s) of Working Experience')
    curr_company =  models.CharField(max_length=50, verbose_name='Current Company')
    curr_title = models.CharField(max_length=50, verbose_name='Title')
    point = models.IntegerField(default=0, verbose_name='Point')
    fav_count = models.IntegerField(default=0, verbose_name='Favourite Count')
    click_count = models.IntegerField(default=0, verbose_name='Click Count')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Instructor Created Time')

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __unicode__(self):
        return self.name