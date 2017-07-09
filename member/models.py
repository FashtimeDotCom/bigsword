# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.rand_char import get_random

# Create your models here.


class Member(AbstractUser):
    nickname=models.CharField(max_length=12, default=u'whoami', verbose_name='nick name')
    is_author=models.BooleanField(default=False, verbose_name='is author')
    has_confirm_email = models.BooleanField(default=True, verbose_name='has confirmed email')
    changepass_code=models.CharField(max_length=16,default=get_random(16))

    class Meta:
        ordering = ['username',]
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

    def __unicode__(self):
        return self.username

    @property
    def name(self):
        return self.last_name + self.first_name

    @property
    def novel_cnt(self):
        if self.is_author is not None:
            return 0