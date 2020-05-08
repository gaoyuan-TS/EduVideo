# _*_coding:utf-8_*_
import json
from smtplib import SMTPRecipientsRefused

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView, logout
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from courses.models import Course
from organization.models import CourseOrg, Teacher
from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from operation.models import UserCourse,UserFavorite,UserMessage
from util.email_send import send_register_email
from util.mixin_utils import LoginRequiredMixin
# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# class LoginView(View):
#     def get(self,request):
#          return render(request, "login.html",{})
#
#     def post(self,request):
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user_name = request.POST.get("username", "")
#             pass_word = request.POST.get("password", "")
#             user = authenticate(username=user_name, password=pass_word)
#             if user is not None:
#                 login(request, user)
#                 return render(request, "index.html", )
#             else:
#                 return render(request, "login.html", {"msg": "用户名或密码错误","login_form":login_form})


class LoginView(View):
    '''用户登录'''

    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', "").strip()
            pass_word = request.POST.get('password', "").strip()
            # 成功返回user对象,失败None
            user = authenticate(request,username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户尚未激活', 'login_form': login_form})
            # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})

        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'login.html',{'login_form':login_form})


class LogoutView(View):
    '''用户登出'''
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email =record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,"active_fail.html")

        return render(request,"login.html")




class RegisterView(View):
    def get(self,request):
        register_form =RegisterForm()
        return render(request,"register.html",{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")
            if UserProfile.objects.filter(email = user_name):
                return render(request,"register.html",{"register_form":register_form,"msg":"用户已存在"})
            pass_word = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = user_name.strip()
            user_profile.email = user_name.strip()
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            #捕捉qq由于邮箱无法找到或拒绝接收，而导致的550错误
            try:
                send_register_email(user_name,"register")
            except SMTPRecipientsRefused as e:
                print('邮箱无法找到或拒绝接收 ', e)
                return render(request, 'register.html', {'register_form': register_form,"msg":"邮箱无法找到或拒绝接收，请更改邮箱地址"})
            else:

                return render(request, 'login.html', {'register_form': register_form,"msg":"发送成功,请激活登录"})
        else:
            return render(request,'register.html',{'register_form':register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            try:
                send_register_email(email,"forget")
            except SMTPRecipientsRefused as e:
                print('邮箱无法找到或拒绝接收 ', e)
                return render(request, "forgetpwd.html", {'forget_form': forget_form,"msg":"邮箱无法找到或拒绝接收，请更改邮箱地址"})
            else:
                return render(request, "forgetpwd.html", {'forget_form': forget_form, "msg": "发送成功,请登录修改密码"})
        else:
            return render(request,"forgetpwd.html",{'forget_form':forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModefyPwdView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", " ")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,"login.html")
        else:
            email = request.POST.get("email", " ")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserinfoView(LoginRequiredMixin,View):
    """
    用户个人信息
    """
    def get(self,request):
        return render(request,'usercenter-info.html',{
        })

    def post(self,request):
        user_info_form =UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    '''用户图像修改'''
    def post(self,request):
        #上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    """
   个人中心修改用户密码
   """
    def post (self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    """
    获取验证码，修改保存邮箱
    """
    def post(self,request):
        email = request.POST.get('email','')
        code  = request.POST.get('code','')

        existed_records =EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user =request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequiredMixin,View):
    """
    我的收藏机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)


        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    """
    我的收藏教师
    """
    def get(self,request):
        teacher_list =[]
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id=fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    """
    我的收藏课程
    """

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })

class MyMessageView(LoginRequiredMixin,View):
    '''我的消息'''

    def get(self, request):
        all_message = UserMessage.objects.filter(user= request.user.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4,request=request)
        messages = p.page(page)
        return  render(request, "usercenter-message.html", {
        "messages":messages,
        })


class IndexView(View):
    """
    首页
    """
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False).order_by('-click_nums')[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs

        })


 # 全局404处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response =render_to_response('404.htlm',{})
    response.status_code=404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
