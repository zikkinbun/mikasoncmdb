from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers

from views import MysqlStatus, MysqlConns, GetMysqlMonitor, CreateMysqlMonitor, \
    UpdateMysqlMonitor, MysqlCom

urlpatterns = [
    url(r'^MysqlStatus$', MysqlStatus.as_view()),
    url(r'^MysqlConns$', MysqlConns.as_view()),
    url(r'^CreateMysqlMonitor$', CreateMysqlMonitor.as_view()),
    url(r'^GetMysqlMonitor$', GetMysqlMonitor.as_view()),
    url(r'^UpdateMysqlMonitor$', UpdateMysqlMonitor.as_view()),
    url(r'^GetMysqlCom$', MysqlCom.as_view()),
]
