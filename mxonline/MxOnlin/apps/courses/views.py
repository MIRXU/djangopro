# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse


from .models import Course,CourseResource
from operation.models import CourseComments,UserCourse
from utils.mixin_util import LoginRequiredMixin

# Create your views here.



class CoursesListView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by('-add_time')

        hot_courses=Course.objects.all().order_by('-click_nums')[:3]
        # 课程排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            # 课程排序
            all_courses = all_courses.order_by('-click_nums')
        # 课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save()

        tag=course.tag
        if tag:
            relate_courses=Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses=[]
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses
        })



class CourseInfoView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        #查询用户是否已经关联了该课程
        user_courses=UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()
        user_courses=UserCourse.objects.filter(course=course)
        user_ids=[ user_course.user.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        course_resources=CourseResource.objects.filter(course=course)
        course_ids=[ user_course.course.id for user_course in all_user_courses]
        relate_courses=Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources':course_resources,
            'relate_courses':relate_courses
        })


class CourseCommentView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_resources = CourseResource.objects.filter(course=course)
        course_comments=CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'course_comments':course_comments
        })



class AddCommentView(View):
    def post(self,request,course_id):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":u"用户未登陆"}', content_type='application/json')
        course_id=request.POST.get('course_id',0)
        comments=request.POST.get('comments','')
        if course_id>0 and comments:
            course_comments=CourseComments()
            course=Course.objects.get(id=int(course_id))
            course_comments.course=course
            course_comments.comments=comments
            course_comments.user=request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":u"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":u"添加失败"}', content_type='application/json')

