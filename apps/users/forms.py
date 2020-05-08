# _*_coding:utf-8_*_
__author__ = 'gy'
__date__ = '2019/5/30 16:51'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    '''登录验证表单'''

    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)



class RegisterForm(forms.Form):
    '''注册验证表单'''
    email =forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha =CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetForm(forms.Form):
    '''忘记密码'''
    email =forms.EmailField(required=True)
    captcha =CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    '''用户更改图像'''
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    '''个人中心信息修改'''
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birthday','address','mobile']