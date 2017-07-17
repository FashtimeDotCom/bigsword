from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.NovelIndexView.as_view(), name='novel_list_home'),
    # url(r'^chapters/(?P<novel_id>[0-9]{1,4})$', views.NovelIndexView.as_view(), name='novel_list'),
    url(r'^chapters/(?P<novel_id>[0-9]{1,4})/(?P<page>[0-9]{1,4})', views.NovelIndexView.as_view(), name='novel_list'),
    url(r'^chapters/detail/(?P<chapter_id>[0-9]{1,4})', views.ChapterDetailView.as_view(), name='chapter_detail'),
    url(r'^chapters/(?P<novel_id>[0-9]{1,4})/(?P<page>[0-9]{1,4})/search', views.SelectItems.as_view(), name='novel_list_search'),
]