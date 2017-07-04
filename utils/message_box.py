#--coding:utf-8--
from django.contrib import messages

class MessageBox(object):
    def __init__(self,warning_tags='bg-warning text-warning', success_tags='bg-info text-info'):
        self.warning_tags = warning_tags
        self.success_tags = success_tags

    def success(self,request,msg):
        return messages.info(request, msg, extra_tags=self.success_tags)

    def warning(self,request,msg):
        return messages.info(request,msg,extra_tags=self.warning_tags)
    def html(self,request,msg):
        pass
