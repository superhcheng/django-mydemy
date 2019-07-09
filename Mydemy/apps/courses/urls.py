# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import CourseListView, CourseOverviewView, CourseCommentsView, CourseVideoListView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^overview/(?P<course_id>\d+)/$', CourseOverviewView.as_view(), name='overview'),
    url(r'^video_list/(?P<course_id>\d+)/$', CourseVideoListView.as_view(), name='video_list'),
    url(r'^comments/(?P<course_id>\d+)/$', CourseCommentsView.as_view(), name='comments'),
]
