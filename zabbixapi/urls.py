# _*_ coding:utf-8_*_
from django.conf.urls import url
from zabbixapi import api
from zabbixapi import agent_api
from zabbixapi import views

app_name = 'zabbixapi'
urlpatterns = [
    url(r'^uptime/$', api.get_uptime, name='get_uptime'),
    url(r'^boottime/$', api.get_boottime, name='get_boottime'),
    url(r'^ping/$', api.agent_ping, name='agent_ping'),
    url(r'^runprocess/$', api.get_runprocess, name='get_runprocess'),
    url(
        r'^cpustat/$',
        views.CpuStatList.as_view()
    ),
    url(
        r'^cpuload/$',
        views.CpuLoadList.as_view()
    ),
    url(
        r'^memstat/$',
        views.MemStatList.as_view()
    ),
]
