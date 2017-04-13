from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers
from . import asset_api

urlpatterns = [
    url(
        r'^list/$',
        asset_api.ServerList.as_view()
    ),
    url(
        r'^detail/(?P<pk>[0-9]+)/$',
        asset_api.ServerDetail.as_view()
    ),
    url(
        r'^delserver/(?P<pk>[0-9]+)/$',
        asset_api.ServerDelete.as_view()
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
