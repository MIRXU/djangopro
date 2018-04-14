# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/2/18 下午8:59'


import xadmin
from .models import UserAsk,CourseComments,UserFavorite,UserMessage,UserCourse


class UserAskAdmin(object):
    list_display=['name','mobile','course_name','add_time']
    search_fields=['name','mobile','course_name']
    list_filter=['name','mobile','course_name','add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course','comments','add_time']
    search_fields = ['user', 'course','comments']
    list_filter = ['user__username','comments','add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id','course','fav_type','add_time']
    search_fields = ['user', 'fav_id','course','fav_type']
    list_filter = ['user__username','fav_id','course','fav_type','add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message','add_time','has_read']
    search_fields = ['user', 'message','has_read']
    list_filter = ['message','add_time','has_read']


class UserCourseAdmin(object):
    list_display = ['user', 'add_time']
    search_fields = ['user']
    list_filter = ['user__username', 'add_time']

xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)