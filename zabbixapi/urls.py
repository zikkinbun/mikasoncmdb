# _*_ coding:utf-8_*_
from django.conf.urls import url
from zabbixapi import api
from zabbixapi import agent_api
from zabbixapi import views

app_name = 'zabbixapi'
urlpatterns = [
    url(r'^UpTime$', api.GetUptime.as_view()),
    url(r'^BootTime$', api.GetBootTime.as_view()),
    url(r'^ping$', agent_api.agent_ping, name='agent_ping'),
    url(r'^RunProcess$', api.GetRunProcess.as_view()),
    url(r'^CpuStat$', views.CpuStatList.as_view()),
    url(r'^CpuLoad$', views.CpuLoadListAll.as_view()),
    url(r'^MemStat$', views.MemStatListAll.as_view()),
    url(r'^CpuLoadByIp$', views.CpuLoadListByIP.as_view()),
    url(r'^MemStatByIp$', views.MemStatListByIP.as_view()),
]
