# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import CourseListView, CourseOverviewView, CourseCommentView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^overview/(?P<course_id>\d+)/$', CourseOverviewView.as_view(), name='overview'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='comment'),
]
