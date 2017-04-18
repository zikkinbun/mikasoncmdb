from django.conf.urls import url
from zabbixapi import api

app_name = 'zabbixapi'
urlpatterns = [
    url(r'^uptime/$', api.get_uptime, name='get_uptime'),
    url(r'^boottime/$', api.get_boottime, name='get_boottime'),
    url(r'^ping/$', api.agent_ping, name='agent_ping'),
    url(r'^runprocess/$', api.get_runprocess, name='get_runprocess'),
]
