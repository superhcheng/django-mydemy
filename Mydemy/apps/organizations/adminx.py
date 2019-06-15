# -*- coding: utf-8 -*-

import xadmin

from .models import City, CourseOrg, Instructor


class CityAdmin(object):
    search_fields = ['name', 'desc']
    list_display = ['name', 'desc', 'create_time']
    list_filter = ['name', 'desc', 'create_time']


class CourseOrgAdmin(object):
    search_fields = ['name', 'desc', 'address', 'city']
    list_display = ['name', 'desc', 'fav_count', 'click_count', 'address', 'city', 'create_time']
    list_filter = ['name', 'desc', 'fav_count', 'click_count', 'address', 'city', 'create_time']


class InstructorAdmin(object):
    search_fields = ['org', 'name', 'work_year', 'curr_company', 'curr_title']
    list_display = ['org', 'name', 'work_year', 'curr_company', 'curr_title', 'point', 'fav_count', 'click_count', 'create_time']
    list_filter = ['org', 'name', 'work_year', 'curr_company', 'curr_title', 'point', 'fav_count', 'click_count', 'create_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Instructor, InstructorAdmin)