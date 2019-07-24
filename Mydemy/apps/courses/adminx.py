# -*- coding: utf-8 -*-
import xadmin

from .models import Course, Lesson, Video, Resource, CourseOnSale


class CourseAdmin(object):
    search_fields = ['name', 'desc', 'difficulty']
    list_display = ['name', 'desc', 'difficulty', 'course_duration']
    list_filter = ['name', 'desc', 'difficulty','student_count', 'fav_count', 'click_count', 'create_time']
    ordering = ['-create_time']
    readonly_fields = ['click_count']
    exclude = ['fav_count']
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        return super(CourseAdmin, self).queryset().filter(on_sale=False)


class CourseOnSaleAdmin(object):
    search_fields = ['name', 'desc', 'difficulty']
    list_display = ['name', 'desc', 'difficulty', 'course_duration']
    list_filter = ['name', 'desc', 'difficulty','student_count', 'fav_count', 'click_count', 'create_time']
    ordering = ['-create_time']
    readonly_fields = ['click_count']
    exclude = ['fav_count']

    def queryset(self):
        return super(CourseOnSaleAdmin, self).queryset().filter(on_sale=True)

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
xadmin.site.register(CourseOnSale, CourseOnSaleAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Resource, ResourceAdmin)