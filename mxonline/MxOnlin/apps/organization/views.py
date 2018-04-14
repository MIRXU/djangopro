# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View

from organization.models import CourseOrg,CityDict
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse

from .forms import UserAskForm
from operation.models import UserFavorite
from organization.models import Teacher
from courses.models import Course

# Create your views here.


class OrgListView(View):
    def get(self,request):
        all_orgs=CourseOrg.objects.all()
        hot_orgs=all_orgs.order_by('-click_nums')[:3]
        all_citys=CityDict.objects.all()
        # 城市搜索
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))
        # 类别搜索
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(catgory=category)
        # 学习人数排序
        sort = request.GET.get('sort', '')
        if sort=='students':
            all_orgs = all_orgs.order_by('-students')
        elif sort=='courses':
        # 课程数量排序
            all_orgs = all_orgs.order_by('-course_nums')
        org_nums = all_orgs.count()
        #课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3,request=request)
        orgs = p.page(page)
        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


class UserAskView(View):
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            print 'ffff'
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":u"添加出错"}',content_type='application/json')


class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = 'home'
        course_org=CourseOrg.objects.get(id=int(org_id))
        fav_has=False
        if request.user.is_authenticated():
           if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
               fav_has=True

        all_courses=course_org.course_set.all()[:3]
        all_teachers=course_org.teacher_set.all()[:1]
        desc=course_org.desc
        org_name=course_org.name
        return  render(request,'org-detail-homepage.html',{
                'all_courses':all_courses,
                'all_teachers':all_teachers,
                'desc':desc,
                'org_name':org_name,
                'course_org':course_org,
                'current_page': current_page,
                'fav_has':fav_has
        })



class OrgCourseView(View):
    def get(self,request,org_id):
        current_page='course'
        course_org=CourseOrg.objects.get(id=int(org_id))
        all_courses=course_org.course_set.all()
        return  render(request,'org-detail-course.html',{
                'all_courses':all_courses,
                'course_org':course_org,
                'current_page':current_page
        })



class OrgDescView(View):
    def get(self,request,org_id):
        current_page='desc'
        course_org=CourseOrg.objects.get(id=int(org_id))
        return  render(request,'org-detail-desc.html',{
                'course_org':course_org,
                'current_page':current_page
        })




class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org=CourseOrg.objects.get(id=int(org_id))
        all_teachers=course_org.teacher_set.all()
        return  render(request,'org-detail-teachers.html',{
                'all_teachers':all_teachers,
                'course_org':course_org,
                'current_page': current_page
        })


class FavView(View):
    """
    收藏功能
    """
    def post(self,request):
        fav_id=request.POST.get('fav_id','0')
        fav_type=request.POST.get('fav_type','')
        #判断用户是否登陆
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":u"用户未登陆"}', content_type='application/json')
        exist_records=UserFavorite.objects.filter(user=request,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #已经收藏，取消
            exist_records.delete()
            return HttpResponse('{"status":"fail","msg":u"收藏"}', content_type='application/json')

        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.fav_id=int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"fail","msg":u"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":u"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teachers=Teacher.objects.all()
        # 点击量排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort=='hot':
                all_teachers = all_teachers.order_by('-click_nums')
        sorted_teacher=Teacher.objects.all().order_by('-click_nums')[:3]
        # 课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)
        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.get(id=teacher_id)
        all_courses=Course.objects.filter(teachers=teacher)
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher
        })





