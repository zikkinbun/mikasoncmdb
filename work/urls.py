# _*_ coding:utf-8_*_
from django.conf.urls import url
from django.contrib import admin
from views import *

app_name = 'work'
urlpatterns = [
    url(r'^editor/$', edit_file, name='edit_file'),
    url(r'^users/$', ServerUserApi.as_view()),
]
