# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime


from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc=models.CharField(max_length=20, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u'城市'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name=models.CharField(max_length=50,verbose_name=u'机构名称')
    catgory=models.CharField(default='pxjg',max_length=20,choices=(('pxjg','培训机构'),('gx','高校'),('ge','个人')),verbose_name=u'机构类别')
    desc=models.TextField(verbose_name=u'机构描述')
    click_nums=models.IntegerField(verbose_name=u'点击数',default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏数', default=0)
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'封面图', max_length=100)
    address=models.CharField(max_length=150,verbose_name=u'机构地址')
    city=models.ForeignKey(CityDict,verbose_name=u'所在城市')
    students=models.IntegerField(verbose_name=u'学习人数', default=0)
    course_nums=models.IntegerField(verbose_name=u'课程数', default=0)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u'课程机构'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name

    #获取机构教师数量
    def get_teachers_nums(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg,verbose_name=u'所属机构')
    name=models.CharField(max_length=50,verbose_name=u'教师名')
    age=models.IntegerField(verbose_name=u'年龄',default=18)
    work_year=models.IntegerField(verbose_name=u'工作年限',default=0)
    work_company=models.CharField(verbose_name=u'就职公司',max_length=50)
    work_position=models.CharField(verbose_name=u'公司职位',max_length=50)
    points=models.CharField(verbose_name=u'教学特点',max_length=50)
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏数', default=0)
    image=models.ImageField(upload_to='teachers/%Y/%m', verbose_name=u'讲师图像', max_length=100,default='')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u'教师'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name