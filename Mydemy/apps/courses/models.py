from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organizations.models import CourseOrg, Instructor


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Course Name')
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, verbose_name='Organization')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Instructor')
    desc = models.CharField(max_length=500, verbose_name='Course Description')
    detail = models.CharField(max_length=100, verbose_name='Course Detail')
    category = models.CharField(max_length=100, default='', verbose_name='Course Category')
    difficulty = models.CharField(max_length=10, choices=(('easy','Easy'), ('medium', 'Medium'),('hard', 'Hard')), verbose_name='Course Difficulty')
    course_duration = models.IntegerField(default=0, verbose_name='Course Duration')
    student_count = models.IntegerField(default=0, verbose_name='Student Count')
    fav_count = models.IntegerField(default=0, verbose_name='Favourite Count')
    click_count = models.IntegerField(default=0, verbose_name='Click Count')
    image = models.ImageField(upload_to='image/courses/course/%Y/%m', default='image/courses/course/default.png', max_length=200, verbose_name='Course Image')
    course_notes = models.CharField(max_length=500, default="", verbose_name='Course Notes')
    course_objectives = models.CharField(max_length=500, default="", verbose_name='Course Objectives')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Course Created Time')

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __unicode__(self):
        return self.name

    def getAllLessons(self):
        return self.lesson_set.all()

    def getAllStudents(self):
        return self.usercourse_set.all()[:5]


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course Name')
    name = models.CharField(max_length=50, verbose_name='Lesson Name')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Lesson Created Time')

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __unicode__(self):
        return self.name

    def get_all_videos(self):
        ret = self.video_set.all()
        return ret


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Lesson Name')
    name = models.CharField(max_length=100, verbose_name='Video Name')
    video_url = models.CharField(max_length=300, default='', verbose_name='Video URL')
    video_duration = models.IntegerField(default=0, verbose_name='Video Duration')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Video Created Time')

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course Name')
    name = models.CharField(max_length=50, verbose_name='Resource Name')
    download = models.FileField(upload_to='file/courses/res/%Y/%m', default='file/courses/res/default.md', verbose_name='Resource Name')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='Resource Created Time')

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    def __unicode__(self):
        return self.name
