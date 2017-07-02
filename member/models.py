# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Member(AbstractUser):
    nickname=models.CharField(max_length=12, default=u'whoami', verbose_name='nick name')
    is_author=models.BooleanField(default=False, verbose_name='is author')

    @property
    def novel_cnt(self):
        if self.is_author is not None:
            return 0