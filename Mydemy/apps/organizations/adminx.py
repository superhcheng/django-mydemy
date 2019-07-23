# -*- coding: utf-8 -*-

import xadmin

from .models import City, CourseOrg, Instructor


class InstructorInline(object):
    model = Instructor
    extra = 0


class CityInline(object):
    model = City
    extra = 0


class CityAdmin(object):
    search_fields = ['name', 'desc']
    list_display = ['name', 'desc', 'create_time']
    list_filter = ['name', 'desc', 'create_time']
    model_icon = 'fa fa-address-book-o'


class CourseOrgAdmin(object):
    search_fields = ['name', 'desc', 'address', 'city']
    list_display = ['name', 'desc', 'fav_count', 'click_count', 'address', 'city', 'create_time']
    list_filter = ['name', 'desc', 'fav_count', 'click_count', 'address', 'city', 'create_time']
    model_icon = 'fa fa-university'
    inlines = [InstructorInline]


class InstructorAdmin(object):
    search_fields = ['org', 'name', 'work_year', 'curr_company', 'curr_title']
    list_display = ['org', 'name', 'work_year', 'curr_company', 'curr_title', 'fav_count', 'click_count', 'create_time']
    list_filter = ['org', 'name', 'work_year', 'curr_company', 'curr_title', 'fav_count', 'click_count', 'create_time']
    model_icon = 'fa fa-users'
    relfield_style = 'fk-ajax'

xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Instructor, InstructorAdmin)