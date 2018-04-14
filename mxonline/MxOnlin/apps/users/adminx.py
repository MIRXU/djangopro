# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/2/18 下午8:59'


import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner
# class UserProfileAdmin(object):
#     list_display = ['nick_name', 'birday', 'gender', 'address','mobile','image']
#     search_fields = ['nick_name', 'birday', 'gender', 'address','mobile']
#     list_filter = ['nick_name', 'birday', 'gender', 'address','mobile','image']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title='我的个人网站管理系统'
    site_footer='个人的公司'
    menu_style='accordion'

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting )