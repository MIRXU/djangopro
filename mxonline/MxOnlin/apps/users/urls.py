# _*_ coding:utf-8 _*_
__author__='xuyijie'
__date__='2018/2/24 下午2:36'


from django.conf.urls import url


from .views import UserInfoView,UploadImageView,ResetPwdView,SendEmailCodeView


urlpatterns = [
    url(r'^list/$', UserInfoView.as_view(),name='user_list'),
    url(r'^image/upload/$', UploadImageView.as_view(),name='image_upload'),
    url(r'^update/pwd/$', ResetPwdView.as_view(),name='update_pwd'),
    #发送邮箱验证码
    url(r'^send_emailcode/$', SendEmailCodeView.as_view(),name='send_emailcode'),
]