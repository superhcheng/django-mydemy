# -*- coding: utf-8 -*-

import xadmin

from .models import UserQuestion, CourseComment, UserFavorite, UserMessage, UserCourse


class UserQuestionAdmin(object):
    search_fields = ['name', 'mobile', 'course_name']
    list_display = ['name', 'mobile', 'course_name', 'create_time']
    list_filter = ['name', 'mobile', 'course_name', 'create_time']


class CourseCommentAdmin(object):
    search_fields = ['user', 'course', 'comment']
    list_display = ['user', 'course', 'comment', 'create_time']
    list_filter = ['user', 'course', 'comment', 'create_time']

class UserFavoriteAdmin(object):
    search_fields = ['user', 'course']
    list_display = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type']


class UserMessageAdmin(object):
    search_fields = ['user', 'message']
    list_display = ['user', 'message', 'has_read' ,'create_time']
    list_filter = ['user', 'message', 'has_read' ,'create_time']


class UserCourseAdmin(object):
    search_fields = ['user', 'course']
    list_display = ['user', 'course', 'create_time']
    list_filter = ['user', 'course', 'create_time']


xadmin.site.register(UserQuestion, UserQuestionAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)