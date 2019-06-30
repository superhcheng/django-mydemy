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
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from Mydemy.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ActivateView, ForgetPwdView, ResetPwdView, DoResetPwdView
from organizations.views import OrgView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url('^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<verification_code>.*)/$', ActivateView.as_view(), name='active'),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^resetpwd/(?P<verification_code>.*)/$', ResetPwdView.as_view(), name="reset_pwd"),
    url(r'^do_resetpwd/$', DoResetPwdView.as_view(), name='do_reset_pwd'),
    url(r'^org_list/$', OrgView.as_view(), name='org_list'),
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
]