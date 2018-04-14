# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/2/22 下午3:13'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误！'})


class ForgetPwdForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误！'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['image']