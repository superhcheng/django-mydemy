# -*- coding: utf-8 -*-
from django.conf.urls import url


from .views import CourseListView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
]
