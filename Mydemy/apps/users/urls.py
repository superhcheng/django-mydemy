"""Mydemy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from users.views import UserInfoView, UpdateUserPwdView, UpdateUserEmailView,UpdateUserAvatarView, \
    UpdateUserEmailGetVCView, UpdateUserProfileView, UserFavCourseView, UserFavInsView, UserFavOrgView, \
    UserCourseView, UserNotificationView


urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    url(r'^update_avatar/', UpdateUserAvatarView.as_view(), name='update_avatar'),
    url(r'^update_pwd/$', UpdateUserPwdView.as_view(), name='update_pwd'),
    url(r'^update_email_vc/$', UpdateUserEmailGetVCView.as_view(), name='update_email_vc'),
    url(r'^update_email/$', UpdateUserEmailView.as_view(), name='update_email'),
    url(r'^update_user/$', UpdateUserProfileView.as_view(), name='update_user'),
    url(r'^fav_course/$', UserFavCourseView.as_view(), name='fav_course'),
    url(r'^fav_ins/$', UserFavInsView.as_view(), name='fav_ins'),
    url(r'^fav_org/$', UserFavOrgView.as_view(), name='fav_org'),
    url(r'^user_course/$', UserCourseView.as_view(), name='user_course'),
    url(r'^user_notification/$', UserNotificationView.as_view(), name='user_notification'),
]