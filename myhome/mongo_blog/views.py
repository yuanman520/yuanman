# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from models import User,Blog,Comment
from django.http import JsonResponse
from django.core.cache import cache

def read_cache(request):
    key = "blog"
    value = cache.get(key)
    if value == None :
        blogs = Blog.objects.all()
        cache.set("blog", blogs)
        if len(blogs) >= 18:
            return render(request, "mongo_blog/first_page.html",
                          {"blogs1": blogs[0:6], "blogs2": blogs[6:12], "blogs3": blogs[12:18]})
        else:
            return render(request, "mongo_blog/first_page.html",
                          {"blogs1": blogs[0:6], "blogs2": blogs[0:6], "blogs3": blogs[0:6]})
    else :
        data=value
        if len(data) >= 18:
            return render(request, "mongo_blog/first_page.html",
                          {"blogs1": data[0:6], "blogs2": data[6:12], "blogs3": data[12:18]})
        else:
            return render(request, "mongo_blog/first_page.html",
                          {"blogs1": data[0:6], "blogs2": data[0:6], "blogs3": data[0:6]})

# def blog(request):
#     blogs=Blog.objects.all()
#     if len(blogs)>=18 :
#         return render(request, "mongo_blog/first_page.html", {"blogs1": blogs[0:6],"blogs2": blogs[6:12],"blogs3": blogs[12:18]})
#     else:
#         return render(request, "mongo_blog/first_page.html", {"blogs1": blogs[0:6],"blogs2": blogs[0:6],"blogs3": blogs[0:6]})

def login(request):
    flag=request.GET.get("out","")
    if flag=="" :
        return render(request, "mongo_blog/login.html", {"msg": ""})
    else :
        return render(request, "mongo_blog/login.html", {"msg": "您已成功安全退出"})

def register(request):
    return render(request,"mongo_blog/register.html")

def page(request,page):
    list=Blog.objects.filter(id=page)
    if len(list)==0:
        return render(request, "mongo_blog/page.html", {"message":"此博客不存在或者被删除"})
    else:
        blog = list[0]
        address=blog.author.address
        comments=Comment.objects.filter(blog=blog)
        return render(request, "mongo_blog/page.html", {"blog": blog,"img":address,"comments":comments})

def mypage(request):
    name = request.POST.get("user", "")
    password=request.POST.get("password","")
    if name=="" or password=="" :
        return render(request, "mongo_blog/login.html", {"msg": "用户名或密码错误"})
    else :
        useremail=User.objects.filter(email=name)
        if len(useremail) == 0 :
            return render(request, "mongo_blog/login.html", {"msg": "用户名不存在"})
        else :
            userpass=useremail[0].password
            user=useremail[0].name
            if userpass==password :
                pen_name=useremail[0].name
                address=useremail[0].address
                blogs=Blog.objects.filter(author=useremail[0])
                return render(request, "mongo_blog/mypage.html",{"pen_name": json.dumps(pen_name),"img":address,"blogs":blogs,"user":user})
            else :
                return render(request, "mongo_blog/login.html", {"msg": "用户名或密码错误"})

def handle(request):
    name=request.GET.get("name","")
    user=request.GET.get("user","")
    password=request.GET.get("password","")
    address=request.GET.get("address","")
    if name=="" or user=="" or password=="" or address=="" :
        return render(request,"mongo_blog/handle.html", {"message":"注册失败，请重新填写信息"})
    else:
        name0=User.objects.filter(name=name)
        user0=User.objects.filter(email=user)
        if len(name0)==0 and len(user0)==0 :
            obj=User(name=name,email=user,password=password,address=address)
            obj.save()
            return render(request, "mongo_blog/handle.html", {"message": "注册成功，请您登录"})
        else :
            return render(request, "mongo_blog/handle.html", {"message": "注册失败，该用户已存在"})

def comment_deal(request):
    text=request.POST.get("text","")
    id=request.POST.get("id","")
    idname=id
    pen_name=request.POST.get("pen_name","")
    if pen_name=="" :
        return render(request, "mongo_blog/login.html", {"msg": "请您先登录"})
    else :
        blog = Blog.objects.filter(id=idname)[0]
        comments=Comment.objects.filter(blog=blog)
        ss=[]
        for acom in comments :
            ss.append(acom.comment_name)
        if pen_name not in ss:
            obj=Comment(blog=blog,comment_name=pen_name,content=text)
            obj.save()
            return render(request, "mongo_blog/comment_deal.html", {"message": "您的评价成功，请您刷新查看"})
        else:
            return render(request, "mongo_blog/comment_deal.html", {"message": "您已经评价过了"})

def write(request):
    name=request.GET.get("name","")
    return render(request, "mongo_blog/write_blog.html",{"name":name})

def deal_handle(request):
    title=request.POST.get("title","")
    author=request.POST.get("author","")
    content = request.POST.get("content","")
    if title=="" or author=="" or content=="" :
        return render(request, "mongo_blog/deal_write.html", {"message":"对不起，您的提交失败"})
    else:
        people=User.objects.filter(name=author)[0]
        obj=Blog(title=title,author=people,content=content)
        obj.save()
        return render(request, "mongo_blog/deal_write.html", {"message":"您的博客上传成功,请返回查看"})

def change(request):
    id=request.GET.get("id","")
    blog=Blog.objects.filter(id=id)[0]
    return render(request, "mongo_blog/change_blog.html",{"blog":blog})

def change_handle(request):
    id = request.POST.get("id", "")
    title = request.POST.get("title", "")
    author = request.POST.get("author", "")
    content = request.POST.get("content", "")
    if title=="" or author=="" or content=="" or id=="":
        return render(request, "mongo_blog/change_handle.html", {"message":"对不起，您的修改失败"})
    else:
        obj=Blog.objects.filter(id=id)
        if len(obj)==0:
            return render(request, "mongo_blog/change_handle.html", {"message": "您的修改失败，请重新操作"})
        else:
            obj.update(title=title,content=content)
            return render(request, "mongo_blog/change_handle.html", {"message": "您的修改成功，请返回查看"})

def delete_handle(request):
    id = request.GET.get("id", "")
    if id :
        obj = Blog.objects.filter(id=id)
        obj.delete()
        dictionary={"success":1 , "message":"删除成功,请返回查看"}
        return JsonResponse(dictionary)
    else :
        return JsonResponse({"success":0 , "message":"删除失败,请您稍后重试"})


































