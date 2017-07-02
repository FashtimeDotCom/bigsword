# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import settings

# Create your models here.


class Chapter(models.Model):
    chapter_name=models.CharField(max_length=24, verbose_name='chapter name')
    chapter_num=models.IntegerField(verbose_name='chapter number')
    created=models.DateTimeField(auto_now_add=True, verbose_name='created time')
    updated=models.DateTimeField(auto_now=True, verbose_name='recent update time')
    content=models.TextField(max_length=10000)
    reader_cnt=models.IntegerField(default=0,verbose_name='readers count')
    novel=models.ForeignKey('Novel',related_name='chapters')

    class Meta:
        verbose_name='Chapter'
        verbose_name_plural='Chapters'
        ordering=['chapter_num',]

    def __unicode__(self):
        return self.chapter_name

    @models.permalink
    def get_absolute_url(self):
        return ('novel:chapter_detail', None, {'c_id':self.pk})


class Novel(models.Model):
    novel_name=models.CharField(max_length=24, verbose_name='novel name')
    description=models.CharField(max_length=200, default=u'这本书懒得介绍自己')
    author=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='novels')
    image=models.ImageField(upload_to='images',null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True, verbose_name='created time')
    reader_cnt=models.IntegerField(default=0, verbose_name='readers count')

    class Meta:
        verbose_name='Novel'
        verbose_name_plural='Novels'
        ordering=['created',]

    def __unicode__(self):
        return self.novel_name

    @property
    def chapter_cnt(self):
        if self.chapters.exists():
            return Chapter.objects.filter(novel_id__exact=self.id).count()
        else:
            return 0

    @property
    def updated(self):
        if self.chapters.exists():
            return Chapter.objects.filter(novel_id__exact=self.id).reverse()[0].updated
        else:
            return 'no chapters updated.'
