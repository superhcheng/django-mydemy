# -*- coding: utf-8 -*-

from django.conf.urls import url

from organizations.views import OrgView, UserRequestView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='list'),
    url(r'^user_request/$', UserRequestView.as_view(), name='user_request'),
]