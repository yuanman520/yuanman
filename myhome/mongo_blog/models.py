# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *
from myhome.settings import DBNAME
import datetime
connect(DBNAME)

class User(Document):
    name=StringField(max_length=30)
    email=EmailField()
    password=StringField(max_length=30)
    address=StringField(max_length=35)

class Blog(Document):
    author=ReferenceField(User,reverse_delete_rule=CASCADE)
    title=StringField(max_length=35)
    content=StringField()
    time=DateTimeField(default=datetime.datetime.now())

class Comment(Document):
    blog=ReferenceField(Blog,reverse_delete_rule=CASCADE)
    comment_name=StringField(max_length=30)
    content=StringField()
    time=DateTimeField(default=datetime.datetime.now())
