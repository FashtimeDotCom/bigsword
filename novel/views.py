# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from models import Novel,Chapter
from utils.paginator import ChapterPaginator

# Create your views here.



class NovelIndexView(TemplateView):
    template_name = 'novel_index.html'
    def get_context_data(self, **kwargs):
        context=super(NovelIndexView, self).get_context_data(**kwargs)
        # 判断novel_id参数是否存在
        if kwargs.has_key('novel_id') and kwargs['novel_id']!='' and kwargs['novel_id']!=None:
            # 判断page参数是否存在
            if kwargs.has_key('page') and kwargs['page']!='' and kwargs['page'] != None:
                paginator = ChapterPaginator(novel_id=kwargs['novel_id'], page_size=4)
                pages = [x for x in range(1, paginator.get_page_cnt() + 1)]
                end = (pages[-1] if len(pages) > 0 else 0)
                page = paginator.check_page(page=int(kwargs['page']),end=end)
                context['end']=end
                context['page']=page
                context['pages']=pages
                context['chapter_list'] = paginator.get_chapters(page,end)
                if paginator.get_page_cnt() > 1:
                    context['errmsg'] = 'OK'
                else:
                    context['errmsg'] = 'Failed'
            # chapter_list=Chapter.objects.filter(novel_id__exact=kwargs['novel_id']).order_by('created')
            current_novel=Novel.objects.get(id=kwargs['novel_id'])
            # context['chapter_list']=chapter_list
            context['current_novel']=current_novel
        novel_list=Novel.objects.all().order_by('reader_cnt').reverse()[:10]
        context['novel_list']=novel_list
        return context


class ChapterListView(TemplateView):
    template_name = 'novel_index.html'
    def get_context_data(self, **kwargs):
        context=super(ChapterListView, self).get_context_data(**kwargs)
        paginator=ChapterPaginator(novel_id=kwargs['novel_id'],page_size=4)
        pages= [x for x in range(1, paginator.get_page_cnt()+1)]
        context['chapter_list'] = paginator.get_chapters(int(kwargs['page']))
        context['page'] = int(kwargs['page'])
        context['end'] = pages[-1]
        context['novel_id'] = kwargs['novel_id']
        if paginator.get_page_cnt()>1:
            context['errmsg']='OK'
        else:
            context['errmsg']='Failed'
        return context