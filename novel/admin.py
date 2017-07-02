# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Novel, Chapter

# Register your models here.

admin.site.register(Novel)
admin.site.register(Chapter)