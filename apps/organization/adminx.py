# _*_coding:utf-8_*_
__author__ = 'gy'
__date__ = '2019/5/30 13:16'

import xadmin

from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums','fav_nums','address','city','add_time']
    search_fields = ['name', 'desc', 'click_nums','fav_nums','address','city']
    list_filter = ['name', 'desc', 'click_nums','fav_nums','address','city','add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'point', 'click_nums','fav_nums','add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'point', 'click_nums','fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'point', 'click_nums','fav_nums','add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)