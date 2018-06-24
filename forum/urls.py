from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='forum'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/list/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/search/$', views.post_search, name='post_search'),
    url(r'^reply/new/(?P<pk>[0-9]+)/$', views.reply_new, name='reply_edit'),
    url(r'^bulletin/new/$', views.bulletin_new, name='bulletin_new'),
    url(r'^message/new/$', views.message_new, name='message_new'),
    url(r'^message/send$', views.message_send, name='message_send'),
    url(r'^message/receive/$', views.message_receive, name='message_receive'),
    url(r'^upload/(?P<pk>[0-9]+)/$', views.upload, name='upload'),
    url(r'^download/(?P<pk>[0-9]+)/$', views.file_down, name='download'),
]