from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers

from mysql_api_views import MysqlStatus, MysqlConns, MysqlCom
from monitor_func_views import CreateMonitorFunction, GetMonitorFunction
from system_api_views import CpuLoadListByIP, MemStatListByIP, GetRunProcess, GetBootTime, GetUptime

urlpatterns = [
    url(r'^MysqlStatus$', MysqlStatus.as_view()),
    url(r'^MysqlConns$', MysqlConns.as_view()),
    url(r'^GetMysqlCom$', MysqlCom.as_view()),
    url(r'^CreateMonFunc$', CreateMonitorFunction.as_view()),
    url(r'^GetMonFunc$', GetMonitorFunction.as_view()),
    url(r'^CpuLoadByIp$', CpuLoadListByIP.as_view()),
    url(r'^MemStatByIp$', MemStatListByIP.as_view()),
    url(r'^RunProcess$', GetRunProcess.as_view()),
    url(r'^UpTime$', GetUptime.as_view()),
    url(r'^BootTime$', GetBootTime.as_view()),
]
