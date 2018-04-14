# _*_ coding:utf-8 _*_
__author__='xuyijie'
__date__='2018/2/24 下午2:36'


from django.conf.urls import url


from courses.views import CoursesListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentView

urlpatterns = [
    url(r'^list/$', CoursesListView.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name='course_detail'),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(),name='course_info'),

    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(),name='course_comment'),

    url(r'^addcomment/$', AddCommentView.as_view(),name='course_addcomment'),
]