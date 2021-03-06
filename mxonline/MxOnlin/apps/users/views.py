# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,UploadImageForm
from utils.email_send import send_register_email
# Create your views here.

from utils.mixin_util import LoginRequiredMixin


class CustonBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email=records.email
                users=UserProfile.objects.get(email=email)
                for user in users:
                    user.is_active=True
                    user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class RegisterView(View):

    """
    用户注册
    """
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})


    def post(self,request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form,'msg': '用户已经存在！'})
            pass_word = request.POST.get('password', '')
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.is_active=False
            user_profile.password=make_password(pass_word)#加密的方法
            user_profile.save()
            send_register_email(user_name,'register')

            return render(request, 'login.html')
        else:
            return render(request, 'register.html',{'register_form':register_form})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def  post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '邮箱未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form':login_form})
# def user_login(request):
#     if request.method=='POST':
#         user_name=request.POST.get('username','')
#         pass_word=request.POST.get('password','')
#         user=authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     elif request.method=='GET':
#         return render(request,'login.html')


class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email=records.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class ModifyPwdView(View):
    """
    修改密码
    """
    def post(self,request):
        modifypwd_form=ModifyPwdForm()
        if modifypwd_form.is_valid():
            password1=request.POST.get('password1','')
            password2 = request.POST.get('password2', '')
            email=request.POST.get('email','')
            if password1!=password2:
                return render(request, 'password_reset.html',{'email':email,'msg':'密码不一致'})
            user=UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()
            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modifypwd_form':modifypwd_form})



class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html')



class UploadImageView(View):
    """
    用户修改图像
    """
    def post(self,request):
        uploadimage_form=UploadImageForm(request.POST,request.FILES,instance=request.user)
        if uploadimage_form.is_valid():
            # uploadimage_form.cleaned_data
            uploadimage_form.save()
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail'}", content_type='application/json')



class ResetPwdView(View):
    """
    重置密码
    """
    def post(self,request):
        modifypwd_form=ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1!=pwd2:
                return HttpResponse("{'status':'fail','msg':'密码不一致'}", content_type='application/json')
            user=request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(modifypwd_form.errors), content_type='application/json')


class SendEmailCodeView(View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email=request.Get.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email':'邮箱已存在'}", content_type='application/json')
        send_register_email(email,'updateemail')
        return HttpResponse("{'status':'success'}", content_type='application/json')


class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))





