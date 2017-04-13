from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers
from . import asset_api

# router = routers.DefaultRouter()
# router.register(r'list', asset_api.ServerListViewSet)
# router.register(r'detail', asset_api.ServerDetailViewSet)

# server_list = asset_api.ServerListViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })
#
# server_detail = asset_api.ServerDetailViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# app_name = 'asset'
#
# urlpatterns = [
#     url(r'^create/$', asset_api.createAsset, name='createAsset'),
# ]
urlpatterns = [
    url(
        r'^list/$',
        asset_api.ServerList.as_view()
    ),
    # url(
    #     r'^detail/(?P<pk>[0-9]+)/$',
    #     server_detail,
    #     name='server_detail'
    # ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
