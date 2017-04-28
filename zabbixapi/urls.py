# _*_ coding:utf-8_*_
from django.conf.urls import url
from zabbixapi import api
from zabbixapi import agent_api

app_name = 'zabbixapi'
urlpatterns = [
    url(r'^uptime/$', api.get_uptime, name='get_uptime'),
    url(r'^boottime/$', api.get_boottime, name='get_boottime'),
    url(r'^ping/$', api.agent_ping, name='agent_ping'),
    url(r'^runprocess/$', api.get_runprocess, name='get_runprocess'),
    url(r'^cpustat/$', agent_api.get_agent_cpu_data, name='get_agent_cpu_data'),
    url(r'^cpuload/$', agent_api.get_agent_cpu_load, name='get_agent_cpu_load'),
]
