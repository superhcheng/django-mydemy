from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


class UserQuestion(models.Model):
    name = models.CharField(max_length=50, verbose_name='Username')
    mobile = models.CharField(max_length=10, verbose_name='Mobile Number', null=True, blank=True)
    course_name = models.CharField(max_length=50, verbose_name='Course Name')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Question Created Time')

    class Meta:
        verbose_name = 'User Question'
        verbose_name_plural = 'User Questions'


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    comment = models.CharField(max_length=1500, verbose_name='Comment')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Comment Created Time')

    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Course Comments'


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    fav_id = models.IntegerField(default=1, verbose_name='Favorite ID')
    fav_type = models.IntegerField(default=1, choices=((1,'Instructor'),(2,'Course'),(3,'Organization')), verbose_name='Favorite Type')

    class Meta:
        verbose_name = 'User Favorite'
        verbose_name_plural = 'User Favorite'


class UserMessage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User')
    message = models.CharField(max_length=1500, verbose_name='Message')
    has_read = models.BooleanField(default=False, verbose_name='Has Read')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Message Created Time')

    class Meta:
        verbose_name = 'User Message'
        verbose_name_plural = 'User Messages'


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Message Created Time')

    class Meta:
        verbose_name = 'User Course Information'
        verbose_name_plural = 'User Course Information'