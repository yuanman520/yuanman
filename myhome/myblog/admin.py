# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import User,Blog,Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Comment)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id","title","author","time")

admin.site.register(Blog,BlogAdmin)
