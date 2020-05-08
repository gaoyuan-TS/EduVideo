# _*_coding:utf-8_*_

from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from operation.models import  UserFavorite
from .forms import UserAskFrom
from courses.models import Course
# Create your views here.


class OrgView(View):
    """
    课程机构列表
    """
    def get(self,request):
        #课程机构
        all_orgs =CourseOrg.objects.all()

        #城市
        all_citys = CityDict.objects.all()
        #取出筛选城市
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords))

        city_id = request.GET.get('city',"")

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category = request.GET.get('ct',"")

        # 热门课程机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:4]
        # 学习人数和课程数筛选


        if category:
            all_orgs = all_orgs.filter(category=category)
        #对课程进行分页

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

         # Provide Paginator with the request object for complete querystring generation
        else:
            p = Paginator(all_orgs, 3,request=request)

            orgs = p.page(page)
            return render(request,"org-list.html",{
                "all_orgs":orgs,
                "all_citys":all_citys,
                "org_nums":org_nums,
                "city_id": city_id,
                "category":category,
                "hot_orgs": hot_orgs,
                "sort": sort,

            })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self,request):
        userask_form = UserAskFrom(request.POST)
        if userask_form.is_valid():
            user_ask =userask_form.save(commit=True)
            return HttpResponse('{"status":"success", "msg":"添加成功"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}',content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav =True

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:3]
        return  render(request, 'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teacher": all_teacher,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav" :has_fav
        })


class OrgCourseView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav":has_fav
        })


class OrgDescView(View):
    '''机构介绍页'''

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            "course_org": course_org,
            "current_page": current_page,
            "has_fav":has_fav,
        })



class OrgTeacherView(View):
    """
   机构教师页
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',{
            "course_org": course_org,
            "all_teacher": all_teacher,
            "current_page":current_page,
            "has_fav":has_fav
        })


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            #如果已经存在则表示用户取消收藏
            exist_record.delete()
            if exist_record:
                # 如果记录已经存在，表示用户取消收藏
                exist_record.delete()
                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums -= 1
                    if org.fav_nums < 0:
                        org.fav_nums = 0
                    org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user =request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return  HttpResponse('{"status":"fail", "msg":"收藏出错"}',content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表
    """
    def get(self,request):
        all_teachers = Teacher.objects.all()
        teacher_nums =all_teachers.count()
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords))

        sort = request.GET.get('sort',"")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:4]
    #分页
        try:
            page =request.GET.get('page',1)
        except:
            page =1
        p = Paginator(all_teachers,5,request=request)

        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teacher':sorted_teacher,
            'teacher_nums':teacher_nums,
            'sort':sort,
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)

        # 教师收藏和机构收藏
        has_teacher_faved =False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'sorted_teacher':sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved,
        })

