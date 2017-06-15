from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index$', views.read_cache),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^page/(\w+)', views.page),
    url(r'^mypage$', views.mypage),
    url(r'^handle$', views.handle),
    url(r'^comment_deal$', views.comment_deal),
    url(r'^write_blog$', views.write),
    url(r'^deal_handle$', views.deal_handle),
    url(r'^change_blog$', views.change),
    url(r'^change_handle$', views.change_handle),
    url(r'^delete_handle$', views.delete_handle),
]