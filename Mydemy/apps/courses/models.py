from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organizations.models import CourseOrg

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Course Name')
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, verbose_name='Organization')
    desc = models.CharField(max_length=500, verbose_name='Course Description')
    detail = models.CharField(max_length=100, verbose_name='Course Detail')
    difficulty = models.CharField(max_length=10, choices=(('easy','Easy'), ('medium', 'Medium'),('hard', 'Hard')), verbose_name='Course Difficulty')
    course_duration = models.IntegerField(default=0, verbose_name='Course Duration')
    student_count = models.IntegerField(default=0, verbose_name='Student Count')
    fav_count = models.IntegerField(default=0, verbose_name='Favourite Count')
    click_count = models.IntegerField(default=0, verbose_name='Click Count')
    image = models.ImageField(upload_to='image/courses/course/%Y/%m', default='image/courses/course/default.png', max_length=200, verbose_name='Course Image')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Course Created Time')

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course Name')
    name = models.CharField(max_length=50, verbose_name='Lesson Name')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Lesson Created Time')

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Lesson Name')
    name = models.CharField(max_length=100, verbose_name='Video Name')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Video Created Time')

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course Name')
    name = models.CharField(max_length=50, verbose_name='Resource Name')
    download = models.FileField(upload_to='file/courses/res/%Y/%m', default='file/courses/res/default.md', verbose_name='Resource Name')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Resource Created Time')

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'