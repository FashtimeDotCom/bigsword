# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,HttpResponseRedirect,reverse
from django.views.generic import View,TemplateView,FormView
from utils.message_box import MessageBox
from member.models import Member
from member.forms import LoginForm,RegisterForm, UserChangePassForm, EmailToChangePassForm, NonUserChangePassForm

# Create your views here.

#TODO: 将url写入环境变量方便管理
class LoginView(FormView):
    failed_url = '/member/login'
    success_url = '/novel'
    form_class = LoginForm
    template_name = 'login.html'
    messages=MessageBox()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.messages.success(request,u'您已经登录,<a href="%s">切换其他账户?</a>' % (reverse('member:member_logout')))
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request,self.template_name, {'form':self.form_class})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=Member.objects.filter(email__exact=email).values('username')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    self.messages.success(request,u'登录成功')
                    return HttpResponseRedirect(self.success_url)
                else:
                    self.messages.warning_tags(request,u'用户未激活')
                    return HttpResponseRedirect(self.failed_url)
            else:
                self.messages.warning(request,u'用户名或密码错误')
                return HttpResponseRedirect(self.failed_url)
        else:
            self.messages.warning(request,u'表单出现错误')
            return HttpResponseRedirect(self.failed_url)


class LogoutView(TemplateView):
    redirect_url = '/member/'
    messages=MessageBox()
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.GET.has_key('next') and request.GET.get('next')=='register':
                self.messages.success(request,u'注销成功')
                logout(request)
                return HttpResponseRedirect(redirect_to=self.redirect_url+'register')
            else:
                self.messages.success(request,u'注销成功，请重新登录')
                logout(request)
                return HttpResponseRedirect(redirect_to=self.redirect_url+'login')
        else:
            self.messages.warning(request,u'您还未登录,请登录')
            return HttpResponseRedirect(redirect_to=self.redirect_url)


class RegisterView(FormView):
    messages=MessageBox()
    logout_url='/member/logout/?next=register'
    login_url = '/member/login'
    register_url='/member/register'
    template_name = 'register.html'
    form_class = RegisterForm

    def __init_form(self,request):
        return render(request,'register.html',{'form':self.form_class()})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.messages.warning(request,u'您 %s 已经登录,请先<a href="%s">注销</a>'%(request.user,self.logout_url))
            return self.__init_form(request)
        else:
            return self.__init_form(request)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            confirm=form.cleaned_data['confirm_password']
            if confirm==password:
                if Member.objects.filter(username__exact=username).exists():
                    self.messages.warning(request,u'用户名已存在')
                    return self.__init_form(request)
                else:
                    if Member.objects.filter(email__exact=email).exists():
                        self.messages.warning(request,u'邮箱已存在')
                        return self.__init_form(request)
                    else:
                        user=Member.objects.create_user(username=username,email=email,password=password)
                        self.messages.success(request,u'注册成功!')
                        return HttpResponseRedirect(self.login_url)
            else:
                self.messages.warning(request,u'两次密码输入不一致')
                return self.__init_form(request)
        else:
            self.messages.warning(request,u'表单出现错误')
            return self.__init_form(request)


class ChangePassView(FormView):
    template_name = 'change_passwd.html'
    redirect_to = '/novel'
    messages = MessageBox()
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            form = UserChangePassForm()
            is_user=True
        else:
            form = EmailToChangePassForm()
            is_user=False
        return render(request,self.template_name,{'form':form,'is_user':is_user})

    def check_password(self,email,old_password,new_password,confirm_password):
        user=Member.objects.get(email__exact=email)
        if authenticate(username=user.username,password=old_password):
            if confirm_password==new_password:
                user.set_password(new_password)
                user.save()
                return (True,u'修改密码成功')
            else:
                return (False,u'两次密码输入不一致')
        else:
            return (False,u'旧密码错误')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            form=UserChangePassForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                old_password=form.cleaned_data['old_password']
                new_password=form.cleaned_data['new_password']
                confirm_password=form.cleaned_data['confirm_password']
                if Member.objects.filter(email__exact=email).exists():
                    check=self.check_password(email,old_password,new_password,confirm_password)
                    if check[0]:
                        self.messages.success(request,check[1])
                        return HttpResponseRedirect(self.redirect_to)
                    else:
                        self.messages.warning(request,check[1])
                        return render(request,self.template_name,{'form':form})
                else:
                    self.messages.warning(request,u'要修改的用户不存在')
            else:
                self.messages.warning(request,u'表单错误')
                return render(request,self.template_name,{'form':form})

