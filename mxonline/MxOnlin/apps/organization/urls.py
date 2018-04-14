# _*_ coding:utf-8 _*_
__author__='xuyijie'
__date__='2018/2/24 下午2:36'


from django.conf.urls import url
from organization.views import OrgListView,UserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,FavView,TeacherListView,TeacherDetailView


urlpatterns = [
    url(r'^list/$', OrgListView.as_view(),name='org_list'),
    url(r'^add_userask/$', UserAskView.as_view(),name='add_userask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(),name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(),name='org_teacher'),
    url(r'^fav/$', FavView.as_view(),name='fav'),

    #讲师列表
    url(r'^teacherlist/$', TeacherListView.as_view(),name='teacher_list'),
    url(r'^teacherdetail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(),name='teacher_detail'),
]