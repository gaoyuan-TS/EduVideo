# _*_coding:utf-8_*_
__author__ = 'gy'
__date__ = '2019/5/30 11:56'
import  xadmin
from xadmin.plugins.auth import UserAdmin
from xadmin import views
from .models import EmailVerifyRecord,Banner,UserProfile


# class UserProfileAdmin(UserAdmin):
#     pass

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = u"后台管理系统"
    site_footer = u"视频在线网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    "显示的字段，搜索的字段范围,过滤器"
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields =['code', 'email', 'send_type']
    list_filter=['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)