# _*_ encoding:utf-8_*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher

from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE,verbose_name=u"课程机构",null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name=u"课程教师",null=True,blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False,verbose_name=u"是否轮播图")
    degree = models.CharField(max_length=2, choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), verbose_name=u"难度")
    learn_time = models.IntegerField(default=0 ,verbose_name=u"学习时长")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y%m", verbose_name=u"封面图片",null=True,blank=True)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=10,default=u"后端开发",verbose_name=u"课程类别")
    tag = models.CharField(default= '',max_length=10,verbose_name=u"关键词",null=True,blank=True)
    youneed_known = models.CharField(default='', max_length=300, verbose_name=u"课程须知",null=True,blank=True)
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u"老师提醒", null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取课程章节数
        return  self.lesson_set.all().count()

    def get_learn_users(self):
        #获取有该课程的其他用户
        return self.usercourse_set.all()[:5]


    def get_course_lesson(self):
        #获取课程的所有章节
        return self.lesson_set.all()


    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_vedio(self):
        #获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频")
    url = models.FileField(upload_to="course/vedio/%Y/%m",null=True,blank=True, verbose_name=u'访问地址')
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长")
    add_time= models.DateTimeField(default=datetime.now , verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,  verbose_name=u"课程名称")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(max_length=100, upload_to="course/resource/%Y/%m", verbose_name="下载")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name