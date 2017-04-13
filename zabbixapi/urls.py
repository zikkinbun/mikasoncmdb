from django.conf.urls import url
from . import views
from zabbixapi import api

app_name = 'zabbixapi'
urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^test_list/$', views.test_list, name='test_list')
]
