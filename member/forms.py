# --coding:utf-8--
from django.forms.models import ModelForm
from django import forms
from .models import Member

class LoginForm(ModelForm):
    email=forms.CharField(label=u'邮箱',widget=forms.EmailInput)
    password=forms.CharField(label=u'密码',widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email','password')


class RegisterForm(ModelForm):
    username=forms.CharField(label=u'用户名')
    email=forms.CharField(label=u'邮箱',widget=forms.EmailInput)
    password=forms.CharField(label=u'密码',widget=forms.PasswordInput)
    confirm_password=forms.CharField(label=u'确认密码',widget=forms.PasswordInput)

    class Meta:
        model=Member
        fields=('username','email','password')
