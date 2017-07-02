from novel.models import Novel,Chapter

class Paginator(object):
    def __init__(self,page_size=10,**kwargs):
        self.page_size=page_size

    def get_page_cnt(self):
        pages=1
        return pages

class ChapterPaginator(Paginator):
    def __init__(self,page_size=10,**kwargs):
        super(ChapterPaginator, self).__init__(**kwargs)
        self.novel_id = kwargs['novel_id']
        self.page_size=page_size

    def get_page_cnt(self):
        num = divmod(Chapter.objects.filter(novel_id__exact=self.novel_id).count(),self.page_size)
        if num[1] != 0:
            pages=num[0]+1
        else:
            pages=num[0]
        return pages

    def check_page(self, page, end):
        if page <= 0:
            page = 1
        elif page > end:
            page=end
        else:
            page=page
        return page

    def get_chapters(self,page,end):
        page=self.check_page(page,end)
        chapter_list = Chapter.objects.filter(novel_id__exact=self.novel_id).order_by('created')[(page-1)*self.page_size:page*self.page_size]
        return chapter_list

