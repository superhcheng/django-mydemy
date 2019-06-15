# -*- coding: utf-8 -*-
import xadmin
from xadmin import views

from .models import UserProfile, UserProfileVerification, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = 'Mydemy Admin Console'
    site_footer = 'Mydemy, Inc.'
    menu_style = 'accordion'

class UserProfileVerificationAdmin(object):
    search_fields = ['code', 'email', 'type']
    list_filter = ['code', 'email', 'type', 'verify_time']
    list_display = ['code', 'email', 'type']


class BannerAdmin(object):
    search_fields = ['title', 'url', 'idx']
    list_filter = ['title', 'url', 'idx', 'create_time']
    list_display = ['title', 'url', 'idx']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(UserProfileVerification, UserProfileVerificationAdmin)
xadmin.site.register(Banner, BannerAdmin)
