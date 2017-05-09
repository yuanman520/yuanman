# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=30)
    address=models.CharField(max_length=35)

    def __unicode__(self):
        return self.name

class Blog(models.Model):
    author=models.ForeignKey(User)
    title=models.CharField(max_length=35)
    content=models.TextField()
    time=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    blog=models.ForeignKey(Blog)
    comment_name=models.CharField(max_length=30)
    content=models.TextField()
    time=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.comment_name
