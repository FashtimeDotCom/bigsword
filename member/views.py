# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,HttpResponseRedirect,reverse
from django.views.generic import View,TemplateView,FormView
from utils.message_box import MessageBox
from member.models import Member
from member.forms import LoginForm

# Create your views here.

class LoginView(FormView):
    failed_url = '/member/login'
    success_url = '/novel'
    form_class = LoginForm
    template_name = 'login.html'
    messages=MessageBox()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.messages.success(request,u'您已经登录,<a href="%s">切换其他账户?</a>'%(reverse('member:member_logout')))
            return HttpResponseRedirect('/novel')
        else:
            form=LoginForm()
            return render(request,self.template_name, {'form':form})
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
    redirect_url = '/member/login'
    messages=MessageBox()
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.messages.success(request,u'注销成功，请重新登录')
            logout(request)
            return HttpResponseRedirect(redirect_to=self.redirect_url)
        else:
            self.messages.warning(request,u'您还未登录,请登录')
            return HttpResponseRedirect(redirect_to=self.redirect_url)


class RegisterView(FormView):
    pass

