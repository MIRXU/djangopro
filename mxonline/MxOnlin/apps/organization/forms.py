# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/2/24 下午2:29'
import re
from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']

    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        REGEX_MOBILE='^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$'
        p=re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码不合法',code='mobile_valida')
