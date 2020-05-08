# _*_coding:utf-8_*_
__author__ = 'gy'
__date__ = '2019/5/30 12:41'

import xadmin
from .models import Course,Lesson,Video,CourseResource

class LessonInline(object):
    model = Lesson
    extra =0

class VideoInline(object):
    model =Video
    extra =0


class CourseAdmin(object):
    list_display = ['name','desc', 'detail', 'degree', 'learn_time','students','add_time']
    search_fields = ['name','desc', 'detail', 'degree', 'learn_time','students']
    list_filter = ['name','desc', 'detail', 'degree', 'learn_time','students','add_time']

    exclude = ['students','fav_nums','click_nums']
    inlines =[LessonInline]
    style_fields ={"detail":"ueditor"}

    def queryset(self):
        # 重载queryset方法，来过滤出我们想要的数据的
        qs = super(CourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程数会少一个
        obj.save()
        # 确定课程的课程机构存在。
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'degree']
    list_filter = ['course', 'name', 'add_time']

    inlines =[VideoInline]

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name', 'degree']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download',]
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
