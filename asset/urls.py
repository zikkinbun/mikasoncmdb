from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers
from . import asset_api, docker_api, docker_init_api

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
    url(
        r'^ckcontain/$',
        docker_init_api.check_containers,
        name='ckcontain'
    ),
    url(
        r'^containlist/$',
        docker_api.ContainerList.as_view()
    ),
    url(
        r'^ckimage/$',
        docker_init_api.check_images,
        name='ckimage'
    ),
    url(
        r'^imagelist/$',
        docker_api.ImageList.as_view()
    ),
    url(
        r'^container/detail/$',
        docker_init_api.inspect_container,
        name='inspect_container'
    ),
    url(
        r'^container/stop/$',
        docker_init_api.stop_container,
        name='stop_container'
    ),
    url(
        r'^container/start/$',
        docker_init_api.start_container,
        name='start_container'
    ),
    url(
        r'^container/delete/$',
        docker_init_api.delete_container,
        name='delete_container'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
