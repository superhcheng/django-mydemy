# -*- coding: utf-8 -*-
import xadmin

from .models import Course, Lesson, Video, Resource


class CourseAdmin(object):
    search_fields = ['name', 'desc', 'difficulty']
    list_display = ['name', 'desc', 'difficulty', 'course_duration']
    list_filter = ['name', 'desc', 'difficulty','student_count', 'fav_count', 'click_count', 'create_time']

class LessonAdmin(object):
    search_fields = ['course', 'name']
    list_display = ['course', 'name', 'create_time']
    list_filter = ['course', 'name', 'create_time']


class VideoAdmin(object):
    search_fields = ['lesson', 'name']
    list_display = ['lesson', 'name', 'create_time']
    list_filter = ['lesson', 'name', 'create_time']


class ResourceAdmin(object):
    search_fields = ['course', 'name', 'download']
    list_display = ['course', 'name', 'download', 'create_time']
    list_filter = ['course', 'name', 'download', 'create_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Resource, ResourceAdmin)